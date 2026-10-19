#!/usr/bin/env python3
"""Convert a georeferenced GeoTIFF DEM into a compact WebGL-ready terrain asset.

Outputs (into ./data by default):
    <ID>.f16      raw little-endian float16 heightmap, row 0 = north
    <ID>.json     metadata (bounds, size, elevation range, resolution ...)
    manifest.json updated list of all converted tiles

Usage:
    python3 scripts/tif2terrain.py tif/N30E120.tif
    python3 scripts/tif2terrain.py tif/*.tif --max-size 2049
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# GeoTIFF tags
TAG_PIXEL_SCALE = 33550
TAG_TIEPOINT = 33922
TAG_GEOKEYS = 34735
TAG_GDAL_NODATA = 42113

METERS_PER_DEG_LAT = 110574.0
METERS_PER_DEG_LON = 111320.0


def _geokeys(tags) -> dict:
    """Parse the GeoKeyDirectory into {key: value} (only short values)."""
    raw = tags.get(TAG_GEOKEYS)
    if not raw:
        return {}
    vals = list(raw)
    if len(vals) < 4:
        return {}
    count = vals[3]
    keys = {}
    for i in range(count):
        base = 4 + i * 4
        if base + 3 >= len(vals):
            break
        key_id, loc, n, value = vals[base : base + 4]
        if loc == 0:
            keys[key_id] = value
    return keys


def _read_georef(tags) -> dict:
    scale = tags.get(TAG_PIXEL_SCALE)
    tie = tags.get(TAG_TIEPOINT)
    if not scale or not tie:
        raise ValueError("TIFF has no ModelPixelScale/ModelTiepoint georeferencing")

    sx, sy = float(scale[0]), float(scale[1])
    tie_i, tie_j, _, tie_x, tie_y = (float(v) for v in tie[:5])
    keys = _geokeys(tags)
    # GTRasterTypeGeoKey: 1 = PixelIsArea, 2 = PixelIsPoint
    raster_type = keys.get(1025, 1)
    epsg = keys.get(3072) or keys.get(2048) or None
    return {
        "pixel_scale": (sx, sy),
        "tiepoint": (tie_i, tie_j, tie_x, tie_y),
        "raster_type": raster_type,
        "epsg": epsg,
    }


def convert(
    tif_path: str,
    out_dir: str = "data",
    max_size: int = 0,
    tile_id: str | None = None,
    smooth: int = 0,
) -> dict:
    with Image.open(tif_path) as im:
        tags = im.tag_v2
        geo = _read_georef(tags)
        arr = np.array(im)
        if arr.ndim == 3:  # single-band tiff opened as grayscale-ish
            arr = arr[..., 0]

        nodata_raw = tags.get(TAG_GDAL_NODATA)
        nodata = None
        if nodata_raw is not None:
            try:
                nodata = float(str(nodata_raw).strip().strip("\x00"))
            except ValueError:
                nodata = None

        arr = arr.astype(np.float64, copy=False)
        valid = np.isfinite(arr)
        if nodata is not None:
            valid &= arr != nodata
        # Treat absurd sentinel values as nodata as well.
        valid &= arr > -12000

        if not valid.any():
            raise ValueError("Raster has no valid elevation samples")

        filled = np.where(valid, arr, 0.0)

        # Optional gentle binomial smoothing (1-2-1 kernel, repeated).
        # SRTM samples contain vegetation / building spikes that look like
        # needles when vertically exaggerated; two passes tame them.
        for _ in range(max(0, smooth)):
            p = np.pad(filled, 1, mode="edge")
            filled = (
                p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:]
                + 2 * p[1:-1, :-2] + 4 * p[1:-1, 1:-1] + 2 * p[1:-1, 2:]
                + p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]
            ) / 16.0

        # Optional area-average downsampling (BOX filter) for lighter assets.
        orig_h, orig_w = filled.shape
        if max_size and max(filled.shape) > max_size:
            h, w = filled.shape
            factor = max_size / max(h, w)
            new_w = max(2, int(round(w * factor)))
            new_h = max(2, int(round(h * factor)))
            img = Image.fromarray(filled.astype(np.float32))
            filled = np.asarray(img.resize((new_w, new_h), Image.BOX), dtype=np.float64)
            valid = np.ones_like(filled, dtype=bool)  # holes already zero-filled
            # Re-apply a light nodata mask so statistics stay sane.
            valid &= filled > -12000
            nodata_count = 0
        else:
            nodata_count = int((~valid).sum())

        heights = np.where(valid, filled, 0.0).astype(np.float32)
        h, w = heights.shape

        sx, sy = geo["pixel_scale"]
        # Keep the real-world extent when the raster was downsampled.
        sx *= orig_w / w
        sy *= orig_h / h
        tie_i, tie_j, tie_x, tie_y = geo["tiepoint"]
        # Bounds of the raster edge (PixelIsArea) or shift by half a pixel
        # when the tiepoint refers to the centre of the first cell.
        west = tie_x - tie_i * sx
        north = tie_y + tie_j * sy
        if geo["raster_type"] == 2:
            west -= 0.5 * sx
            north += 0.5 * sy
        east = west + w * sx
        south = north - h * sy
        lon0 = (west + east) * 0.5
        lat0 = (south + north) * 0.5

        width_m = w * sx * METERS_PER_DEG_LON * math.cos(math.radians(lat0))
        depth_m = h * sy * METERS_PER_DEG_LAT

        # Fill remaining holes with sea level; shader treats 0 as low ground.
        heights[~valid] = 0.0

        tile_id = tile_id or os.path.splitext(os.path.basename(tif_path))[0]
        os.makedirs(out_dir, exist_ok=True)
        bin_path = os.path.join(out_dir, f"{tile_id}.f16")
        heights.astype("<f2").tofile(bin_path)

        meta = {
            "id": tile_id,
            "name": tile_id,
            "source": os.path.relpath(tif_path, os.getcwd()),
            "format": "float16le",
            "width": int(w),
            "height": int(h),
            "bounds": {
                "west": round(west, 9),
                "south": round(south, 9),
                "east": round(east, 9),
                "north": round(north, 9),
            },
            "center": [round(lon0, 9), round(lat0, 9)],
            "pixelSize": [round(sx, 12), round(sy, 12)],
            "sizeMeters": [round(width_m, 1), round(depth_m, 1)],
            "minElevation": round(float(heights.min()), 2),
            "maxElevation": round(float(heights.max()), 2),
            "meanElevation": round(float(heights.mean()), 2),
            "nodata": nodata,
            "nodataPixels": nodata_count,
            "crs": f"EPSG:{geo['epsg']}" if geo["epsg"] else "unknown",
            "verticalDatum": "EGM96 (assumed)",
            "bytes": os.path.getsize(bin_path),
        }
        meta_path = os.path.join(out_dir, f"{tile_id}.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        _update_manifest(out_dir, meta)
    return meta


def _update_manifest(out_dir: str, meta: dict) -> None:
    manifest_path = os.path.join(out_dir, "manifest.json")
    tiles = []
    default = None
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, encoding="utf-8") as f:
                data = json.load(f)
            tiles = data.get("tiles", [])
            default = data.get("default")
        except (OSError, ValueError):
            tiles = []
    summary = {
        "id": meta["id"],
        "name": meta["name"],
        "file": f"{meta['id']}.f16",
        "meta": f"{meta['id']}.json",
        "width": meta["width"],
        "height": meta["height"],
        "minElevation": meta["minElevation"],
        "maxElevation": meta["maxElevation"],
        "center": meta["center"],
        "sizeMeters": meta["sizeMeters"],
        "bounds": meta["bounds"],
    }
    tiles = [t for t in tiles if t.get("id") != meta["id"]]
    tiles.append(summary)
    tiles.sort(key=lambda t: t["id"])
    ids = {t["id"] for t in tiles}
    default = default if default in ids else meta["id"]
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"tiles": tiles, "default": default}, f, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tifs", nargs="+", help="GeoTIFF DEM file(s)")
    parser.add_argument("--out", default="data", help="output directory (default: data)")
    parser.add_argument(
        "--max-size",
        type=int,
        default=0,
        help="downsample so the longest side is at most this many samples (0 = keep)",
    )
    parser.add_argument("--id", help="override tile id (single input only)")
    parser.add_argument(
        "--smooth",
        type=int,
        default=2,
        help="binomial smoothing passes for the heightmap (default: 2, 0 = raw)",
    )
    args = parser.parse_args()

    for path in args.tifs:
        try:
            meta = convert(path, args.out, args.max_size, args.id, args.smooth)
        except Exception as exc:  # noqa: BLE001 - CLI should keep going
            print(f"[error] {path}: {exc}", file=sys.stderr)
            continue
        print(
            f"[ok] {meta['id']}: {meta['width']}x{meta['height']} "
            f"{meta['minElevation']}..{meta['maxElevation']} m "
            f"({meta['bytes'] / 1048576:.1f} MB)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
