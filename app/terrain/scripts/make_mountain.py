#!/usr/bin/env python3
"""Generate a local 10 km-radius mountain terrain asset from 1° GeoTIFF tiles.

Example (太子尖 / Taizi Jian):
    python3 scripts/make_mountain.py \
        --id C327 --name 太子尖 --lon 118.89967 --lat 30.17559 --radius 10

Outputs:
    data/mountains/C327/heightmap.f16   float16 heightmap, row 0 = north
    data/mountains/C327/meta.json       bounds, peak elevation, source tiles ...
    data/mountains/catalog.json         updated list used by /mountain/terrain

The output grid is square in *meters* around the peak, so the 3D terrain is not
distorted by longitude convergence.  The source 1x1 degree tiles are stitched
when the requested radius crosses a tile boundary.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

METERS_PER_DEG_LAT = 110574.0
METERS_PER_DEG_LON = 111320.0

TAG_PIXEL_SCALE = 33550
TAG_TIEPOINT = 33922
TAG_GEOKEYS = 34735
TAG_GDAL_NODATA = 42113

ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def geokeys(tags) -> dict:
    raw = tags.get(TAG_GEOKEYS)
    if not raw:
        return {}
    vals = list(raw)
    if len(vals) < 4:
        return {}
    keys = {}
    for i in range(vals[3]):
        base = 4 + i * 4
        if base + 3 >= len(vals):
            break
        key_id, loc, _count, value = vals[base : base + 4]
        if loc == 0:
            keys[key_id] = value
    return keys


def tile_name(lat_i: int, lon_i: int) -> str:
    ns = "N" if lat_i >= 0 else "S"
    ew = "E" if lon_i >= 0 else "W"
    return f"{ns}{abs(lat_i):02d}{ew}{abs(lon_i):03d}.tif"


class Tile:
    def __init__(self, path: Path):
        self.path = path
        with Image.open(path) as im:
            tags = im.tag_v2
            scale = tags.get(TAG_PIXEL_SCALE)
            tie = tags.get(TAG_TIEPOINT)
            if not scale or not tie:
                raise ValueError(f"{path}: missing ModelPixelScale/ModelTiepoint")
            self.sx = float(scale[0])
            self.sy = float(scale[1])
            tie_i, tie_j, _tie_z, tie_x, tie_y = (float(v) for v in tie[:5])
            keys = geokeys(tags)
            raster_type = keys.get(1025, 1)  # 1=Area, 2=Point
            self.west = tie_x - tie_i * self.sx
            self.north = tie_y + tie_j * self.sy
            if raster_type == 2:
                self.west -= 0.5 * self.sx
                self.north += 0.5 * self.sy
            self.epsg = keys.get(3072) or keys.get(2048)

            nodata_raw = tags.get(TAG_GDAL_NODATA)
            nodata = None
            if nodata_raw is not None:
                try:
                    nodata = float(str(nodata_raw).strip().strip("\x00"))
                except ValueError:
                    nodata = None

            arr = np.array(im)
            if arr.ndim == 3:
                arr = arr[..., 0]
            self.arr = arr.astype(np.float32, copy=False)
            self.height, self.width = self.arr.shape
            self.east = self.west + self.width * self.sx
            self.south = self.north - self.height * self.sy

            valid = np.isfinite(self.arr) & (self.arr > -12000)
            if nodata is not None:
                valid &= self.arr != nodata
            self.valid = valid
            self.nodata = nodata

    def __repr__(self) -> str:
        return f"Tile({self.path.name}, {self.width}x{self.height})"


class TileCache:
    """Small LRU cache of decoded tiles (each ~65 MB in memory)."""

    def __init__(self, max_tiles: int = 6):
        self.max_tiles = max(1, max_tiles)
        self._cache: OrderedDict[str, Tile] = OrderedDict()

    def get(self, path: Path) -> Tile:
        key = str(path)
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        print(f"[tile] load {path.name}", flush=True)
        tile = Tile(path)
        print(
            f"       {tile.width}x{tile.height}  "
            f"{tile.west:.4f}..{tile.east:.4f}E  "
            f"{tile.south:.4f}..{tile.north:.4f}N",
            flush=True,
        )
        self._cache[key] = tile
        while len(self._cache) > self.max_tiles:
            self._cache.popitem(last=False)
        return tile

    def __len__(self) -> int:
        return len(self._cache)


def binomial_smooth(a: np.ndarray, passes: int) -> np.ndarray:
    for _ in range(max(0, passes)):
        p = np.pad(a, 1, mode="edge")
        a = (
            p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:]
            + 2 * p[1:-1, :-2] + 4 * p[1:-1, 1:-1] + 2 * p[1:-1, 2:]
            + p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]
        ) / 16.0
    return a


def fill_holes(a: np.ndarray, rounds: int = 80) -> tuple[np.ndarray, int]:
    """Nearest-ish fill for nodata holes (edge dilation average)."""
    holes = ~np.isfinite(a)
    count = int(holes.sum())
    if count == 0:
        return a, 0
    out = a.copy()
    out[holes] = np.nanmean(a)
    for _ in range(rounds):
        holes = ~np.isfinite(out)
        if not holes.any():
            break
        p = np.pad(out, 1, mode="edge")
        neighbours = np.stack(
            [p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]], axis=0
        )
        mean = np.nanmean(neighbours, axis=0)
        out = np.where(holes, mean, out)
    return np.nan_to_num(out, nan=0.0), count


def build(
    tif_dir: Path,
    out_dir: Path,
    mountain_id: str,
    name: str,
    lon: float,
    lat: float,
    radius_km: float,
    size: int,
    smooth: int,
    record: dict | None = None,
    tile_cache: "TileCache | None" = None,
    write_catalog: bool = True,
    verbose: bool = True,
) -> dict:
    if not ID_RE.match(mountain_id):
        raise ValueError("ID 只能包含字母、数字、下划线和短横线（1–64 字符）")
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        raise ValueError("经纬度超出范围")
    if radius_km <= 0:
        raise ValueError("半径必须大于 0")
    if size % 2 == 0:
        size += 1
        if verbose:
            print(f"[info] 采样数调整为奇数 {size}，以保证峰值正好位于中心像素")
    if size < 65:
        raise ValueError("采样数至少为 65")

    radius_m = radius_km * 1000.0
    m_per_deg_lon = METERS_PER_DEG_LON * math.cos(math.radians(lat))
    m_per_deg_lat = METERS_PER_DEG_LAT
    half_lon = radius_m / m_per_deg_lon
    half_lat = radius_m / m_per_deg_lat
    west, east = lon - half_lon, lon + half_lon
    south, north = lat - half_lat, lat + half_lat

    lat_i_min = math.floor(south + 1e-9)
    lat_i_max = math.floor(north - 1e-9)
    lon_i_min = math.floor(west + 1e-9)
    lon_i_max = math.floor(east - 1e-9)

    tile_paths = []
    missing = []
    for lat_i in range(lat_i_min, lat_i_max + 1):
        for lon_i in range(lon_i_min, lon_i_max + 1):
            path = tif_dir / tile_name(lat_i, lon_i)
            if path.exists():
                tile_paths.append(path)
            else:
                missing.append(path.name)
    if missing:
        raise FileNotFoundError(
            f"缺少覆盖该区域的高程瓦片: {', '.join(missing)}（目录: {tif_dir}）"
        )

    if verbose:
        print(f"[info] 峰值 {name} ({mountain_id}) {lon:.5f}, {lat:.5f} 半径 {radius_km:g} km")
        print(f"[info] 地理范围 {west:.5f}..{east:.5f}E, {south:.5f}..{north:.5f}N")
        print(f"[info] 需要瓦片: {', '.join(p.name for p in tile_paths)}")

    tiles = []
    for path in tile_paths:
        if tile_cache is None:
            if verbose:
                print(f"[info] 读取 {path} …", flush=True)
            tile = Tile(path)
            if verbose:
                print(
                    f"       {tile.width}x{tile.height}  "
                    f"{tile.west:.4f}..{tile.east:.4f}E  "
                    f"{tile.south:.4f}..{tile.north:.4f}N"
                )
        else:
            tile = tile_cache.get(path)
        tiles.append(tile)

    # Output grid: square in metres, row 0 = north.
    east_m = (np.arange(size, dtype=np.float64) / (size - 1) - 0.5) * (2 * radius_m)
    north_m = (0.5 - np.arange(size, dtype=np.float64) / (size - 1)) * (2 * radius_m)
    lon_grid = lon + np.broadcast_to(east_m[None, :], (size, size)) / m_per_deg_lon
    lat_grid = lat + np.broadcast_to(north_m[:, None], (size, size)) / m_per_deg_lat

    heights = np.full((size, size), np.nan, dtype=np.float32)
    for tile in tiles:
        mask = (
            (lon_grid >= tile.west) & (lon_grid < tile.east)
            & (lat_grid > tile.south) & (lat_grid <= tile.north)
        )
        if not mask.any():
            continue
        lons = lon_grid[mask]
        lats = lat_grid[mask]
        col = (lons - tile.west) / tile.sx - 0.5
        row = (tile.north - lats) / tile.sy - 0.5
        inside = (
            (col >= 0) & (col <= tile.width - 1)
            & (row >= 0) & (row <= tile.height - 1)
        )
        if not inside.any():
            continue

        c = col[inside]
        r = row[inside]
        c0 = np.floor(c).astype(np.int32)
        r0 = np.floor(r).astype(np.int32)
        c1 = np.minimum(c0 + 1, tile.width - 1)
        r1 = np.minimum(r0 + 1, tile.height - 1)
        fc = (c - c0).astype(np.float32)
        fr = (r - r0).astype(np.float32)

        v00 = tile.arr[r0, c0]
        v10 = tile.arr[r0, c1]
        v01 = tile.arr[r1, c0]
        v11 = tile.arr[r1, c1]
        ok = (
            tile.valid[r0, c0] & tile.valid[r0, c1]
            & tile.valid[r1, c0] & tile.valid[r1, c1]
        )
        sampled = (
            v00 * (1 - fc) * (1 - fr)
            + v10 * fc * (1 - fr)
            + v01 * (1 - fc) * fr
            + v11 * fc * fr
        )
        vals = np.full(lons.shape, np.nan, dtype=np.float32)
        vals[inside] = np.where(ok, sampled, np.nan)

        target = heights[mask]
        heights[mask] = np.where(np.isnan(target), vals, target)

    holes = int((~np.isfinite(heights)).sum())
    if holes:
        print(f"[warn] {holes} 个采样点无有效高程，按邻近值填充")
        heights, _ = fill_holes(heights)
    heights = binomial_smooth(heights, smooth).astype(np.float32)

    center = (size - 1) // 2
    peak_elevation = float(heights[center, center])
    min_elev = float(heights.min())
    max_elev = float(heights.max())
    max_r, max_c = np.unravel_index(int(np.argmax(heights)), heights.shape)
    max_lon = lon + east_m[max_c] / m_per_deg_lon
    max_lat = lat + north_m[max_r] / m_per_deg_lat

    mountain_dir = out_dir / mountain_id
    mountain_dir.mkdir(parents=True, exist_ok=True)
    bin_path = mountain_dir / "heightmap.f16"
    heights.astype("<f2").tofile(bin_path)

    resolution = 2 * radius_m / (size - 1)
    epsg = tiles[0].epsg if tiles else None
    meta = {
        "id": mountain_id,
        "name": name,
        "type": "mountain",
        "format": "float16le",
        "width": size,
        "height": size,
        "radiusKm": radius_km,
        "center": [round(lon, 8), round(lat, 8)],
        "bounds": {
            "west": round(west, 9),
            "south": round(south, 9),
            "east": round(east, 9),
            "north": round(north, 9),
        },
        "sizeMeters": [round(2 * radius_m, 1), round(2 * radius_m, 1)],
        "resolutionMeters": round(resolution, 2),
        "minElevation": round(min_elev, 2),
        "maxElevation": round(max_elev, 2),
        "peakElevation": round(peak_elevation, 2),
        "peak": {
            "lon": round(lon, 8),
            "lat": round(lat, 8),
            "elevation": round(peak_elevation, 2),
            "world": [0.0, round(peak_elevation, 2), 0.0],
        },
        "cropMaximum": {
            "lon": round(float(max_lon), 8),
            "lat": round(float(max_lat), 8),
            "elevation": round(max_elev, 2),
        },
        "sourceTiles": [str(p).replace(os.sep, "/") for p in tile_paths],
        "crs": f"EPSG:{epsg}" if epsg else "EPSG:4326",
        "verticalDatum": "EGM96 (assumed)",
        "smoothPasses": smooth,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bytes": os.path.getsize(bin_path),
    }

    if record is not None:
        meta["record"] = record
        try:
            meta["listedHeight"] = round(float(record.get("height")), 2)
        except (TypeError, ValueError):
            pass
        if record.get("timezone") is not None:
            meta["timezone"] = record.get("timezone")
        if record.get("source") is not None:
            meta["source"] = record.get("source")
        if record.get("elevations") is not None:
            meta["elevations"] = record.get("elevations")

    meta_path = mountain_dir / "meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    if write_catalog:
        update_catalog(out_dir, meta)
    if verbose:
        print(
            f"[ok] {name} ({mountain_id}) {size}x{size}  "
            f"{min_elev:.1f}..{max_elev:.1f} m  峰值 {peak_elevation:.1f} m  "
            f"({bin_path.stat().st_size / 1048576:.1f} MB)"
        )
        print(f"[ok] {bin_path}")
        print(f"[ok] {meta_path}")
    return meta


def catalog_sort_key(mountain_id):
    match = re.match(r"^([A-Za-z_-]+)(\d+)$", str(mountain_id))
    if match:
        return (match.group(1).upper(), int(match.group(2)))
    return (str(mountain_id).upper(), 0)


def _catalog_entry(meta: dict) -> dict:
    return {
        "id": meta["id"],
        "name": meta["name"],
        "lon": meta["center"][0],
        "lat": meta["center"][1],
        "peakElevation": meta["peakElevation"],
        "listedHeight": meta.get("listedHeight"),
        "minElevation": meta["minElevation"],
        "maxElevation": meta["maxElevation"],
        "radiusKm": meta["radiusKm"],
        "sizeMeters": meta["sizeMeters"],
        "width": meta.get("width"),
        "height": meta.get("height"),
        "timezone": meta.get("timezone"),
        "source": meta.get("source"),
        "updated": meta["generatedAt"],
    }


def merge_catalog(out_dir: Path, metas: list[dict]) -> None:
    """Merge one or many peak metadata records into catalog.json once."""
    if not metas:
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    catalog_path = out_dir / "catalog.json"
    mountains = []
    default = None
    if catalog_path.exists():
        try:
            with open(catalog_path, encoding="utf-8") as f:
                data = json.load(f)
            mountains = data.get("mountains", [])
            default = data.get("default")
        except (OSError, ValueError):
            mountains = []

    by_id = {m.get("id"): m for m in mountains if m.get("id")}
    for meta in metas:
        by_id[meta["id"]] = _catalog_entry(meta)
    mountains = sorted(by_id.values(), key=lambda m: catalog_sort_key(m.get("id", "")))
    ids = {m["id"] for m in mountains}
    if default not in ids:
        default = metas[-1]["id"]
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "mountains": mountains,
                "default": default,
                "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def update_catalog(out_dir: Path, meta: dict) -> None:
    merge_catalog(out_dir, [meta])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, help="山峰 ID，如 C327")
    parser.add_argument("--name", help="山峰名称，默认使用 ID")
    parser.add_argument("--lon", type=float, required=True, help="经度（WGS84）")
    parser.add_argument("--lat", type=float, required=True, help="纬度（WGS84）")
    parser.add_argument("--radius", type=float, default=10.0, help="半径（km），默认 10")
    parser.add_argument("--size", type=int, default=1025, help="输出采样数（奇数），默认 1025")
    parser.add_argument("--smooth", type=int, default=2, help="二项式平滑次数，默认 2")
    parser.add_argument("--tif-dir", default="tif", help="源 1° GeoTIFF 目录")
    parser.add_argument("--out", default="data/mountains", help="输出目录")
    args = parser.parse_args()

    name = args.name or args.id
    try:
        build(
            tif_dir=Path(args.tif_dir),
            out_dir=Path(args.out),
            mountain_id=args.id,
            name=name,
            lon=args.lon,
            lat=args.lat,
            radius_km=args.radius,
            size=args.size,
            smooth=args.smooth,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
