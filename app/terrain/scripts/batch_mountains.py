#!/usr/bin/env python3
"""Generate terrain assets for *every* peak in a mountain-list JSON file.

The input schema matches mountainlist_china02.json:

    {
      "name": "玉山",
      "latitude": "23.47",
      "longitude": "120.957222222",
      "height": "3952",
      "source": 3,
      "mountainId": "T1",
      "timezone": "Asia/Taipei",
      "elevations": ["1933", "3000", "3952"]
    }

Usage (from the project root):

    python3 scripts/batch_mountains.py \
        --json /path/to/mountainlist_china02.json \
        --size 1025

    # resume an interrupted run
    python3 scripts/batch_mountains.py \
        --json /path/to/mountainlist_china02.json \
        --size 1025 --skip-existing

The source tiles are cached in a small LRU (default 6 tiles ≈ 400 MB) and
peaks are processed in spatial order so neighbouring peaks reuse tiles.
The catalog is written once at the end.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

from make_mountain import (
    ID_RE,
    METERS_PER_DEG_LAT,
    METERS_PER_DEG_LON,
    TileCache,
    build,
    merge_catalog,
    tile_name,
)

ROOT = Path(__file__).resolve().parent.parent


def required_tiles(lon: float, lat: float, radius_km: float) -> list[str]:
    radius_m = radius_km * 1000.0
    m_per_deg_lon = METERS_PER_DEG_LON * math.cos(math.radians(lat))
    half_lon = radius_m / m_per_deg_lon
    half_lat = radius_m / METERS_PER_DEG_LAT
    west, east = lon - half_lon, lon + half_lon
    south, north = lat - half_lat, lat + half_lat
    names = []
    for yi in range(math.floor(south + 1e-9), math.floor(north - 1e-9) + 1):
        for xi in range(math.floor(west + 1e-9), math.floor(east - 1e-9) + 1):
            names.append(tile_name(yi, xi))
    return names


def load_peaks(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("mountains") or data.get("data") or data.get("peaks")
    if not isinstance(data, list):
        raise ValueError("JSON 顶层应该是山峰数组（或包含 mountains/data/peaks 数组的对象）")

    peaks: dict[str, dict] = {}
    for index, raw in enumerate(data):
        if not isinstance(raw, dict):
            print(f"[warn] 第 {index} 条不是对象，跳过", file=sys.stderr)
            continue
        mid = str(raw.get("mountainId") or raw.get("id") or "").strip()
        name = str(raw.get("name") or mid).strip() or mid
        try:
            lon = float(raw["longitude"])
            lat = float(raw["latitude"])
        except (KeyError, TypeError, ValueError):
            print(f"[warn] {mid or index}: 经纬度缺失或无效，跳过", file=sys.stderr)
            continue
        if not ID_RE.match(mid):
            print(f"[warn] {mid or index}: ID 无效，跳过", file=sys.stderr)
            continue
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            print(f"[warn] {mid}: 经纬度超出范围，跳过", file=sys.stderr)
            continue
        if mid in peaks:
            print(f"[warn] {mid}: ID 重复，保留最后一条", file=sys.stderr)
        peaks[mid] = {
            "id": mid,
            "name": name,
            "lon": lon,
            "lat": lat,
            "raw": raw,
        }
    return list(peaks.values())


def spatial_key(peak: dict):
    # Process one 1° cell at a time to maximise TileCache hits.
    return (
        math.floor(peak["lat"]),
        math.floor(peak["lon"]),
        -peak["lat"],
        peak["lon"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", required=True, help="山峰列表 JSON 路径")
    parser.add_argument("--out", default="data/mountains", help="输出目录")
    parser.add_argument("--tif-dir", default="tif", help="源 1° GeoTIFF 目录")
    parser.add_argument("--radius", type=float, default=10.0, help="半径 km，默认 10")
    parser.add_argument(
        "--size",
        type=int,
        default=1025,
        help="输出采样数（奇数）。1025 ≈ 2.0 MB/峰；513 ≈ 0.5 MB/峰",
    )
    parser.add_argument("--smooth", type=int, default=2, help="平滑次数，默认 2")
    parser.add_argument("--tile-cache", type=int, default=6, help="缓存源瓦片数，默认 6")
    parser.add_argument("--limit", type=int, default=0, help="只处理前 N 条（调试用）")
    parser.add_argument("--skip-existing", action="store_true", help="跳过已生成的山峰（可断点续跑）")
    parser.add_argument("--dry-run", action="store_true", help="只检查瓦片覆盖，不生成文件")
    parser.add_argument("--traceback", action="store_true", help="失败时打印完整 traceback")
    parser.add_argument("--progress", type=int, default=20, help="每 N 条打印一次进度")
    args = parser.parse_args()

    os.chdir(ROOT)
    json_path = Path(args.json).expanduser().resolve()
    out_dir = Path(args.out)
    tif_dir = Path(args.tif_dir)

    peaks = load_peaks(json_path)
    if args.limit:
        peaks = peaks[: args.limit]
    peaks.sort(key=spatial_key)
    total = len(peaks)
    if not total:
        print("[error] JSON 中没有可用山峰", file=sys.stderr)
        return 1

    missing_refs = 0
    missing_peaks = 0
    tile_set = set()
    for peak in peaks:
        names = required_tiles(peak["lon"], peak["lat"], args.radius)
        tile_set.update(names)
        missing = [n for n in names if not (tif_dir / n).exists()]
        if missing:
            missing_peaks += 1
            missing_refs += len(missing)
            print(f"[missing] {peak['id']} {peak['name']}: {', '.join(missing)}")
    print(
        f"[info] 山峰 {total} 座 · 需要 {len(tile_set)} 块 1° 瓦片 · "
        f"缺失 {missing_refs} 块 / 影响 {missing_peaks} 座"
    )
    if args.size % 2 == 0:
        print(f"[info] size 将调整为奇数 {args.size + 1}")
    estimate = total * (args.size + 1) ** 2 * 2 / 1048576
    print(f"[info] 预计高程数据约 {estimate:.0f} MB（不含 meta/catalog）")
    if args.dry_run:
        return 0 if missing_refs == 0 else 1

    cache = TileCache(max_tiles=args.tile_cache)
    results: list[dict] = []
    failures: list[dict] = []
    generated = skipped = 0
    started = time.time()

    for index, peak in enumerate(peaks, 1):
        mid = peak["id"]
        meta_path = out_dir / mid / "meta.json"
        bin_path = out_dir / mid / "heightmap.f16"
        if args.skip_existing and meta_path.exists() and bin_path.exists():
            try:
                with open(meta_path, encoding="utf-8") as f:
                    meta = json.load(f)
                results.append(meta)
                skipped += 1
                print(f"[skip] {mid} {peak['name']}", flush=True)
            except (OSError, ValueError) as exc:
                print(f"[warn] {mid}: 已存在文件无法读取（{exc}），重新生成", file=sys.stderr)
            else:
                if index % args.progress == 0 or index == total:
                    elapsed = time.time() - started
                    rate = index / elapsed if elapsed else 0
                    eta = (total - index) / rate if rate else 0
                    print(
                        f"[{index}/{total}] {elapsed / 60:.1f} min · ETA {eta / 60:.1f} min · "
                        f"ok {generated} · skip {skipped} · fail {len(failures)}",
                        flush=True,
                    )
                continue

        try:
            meta = build(
                tif_dir=tif_dir,
                out_dir=out_dir,
                mountain_id=mid,
                name=peak["name"],
                lon=peak["lon"],
                lat=peak["lat"],
                radius_km=args.radius,
                size=args.size,
                smooth=args.smooth,
                record=peak["raw"],
                tile_cache=cache,
                write_catalog=False,
                verbose=False,
            )
            results.append(meta)
            generated += 1
        except Exception as exc:  # noqa: BLE001
            failures.append({"id": mid, "name": peak["name"], "error": str(exc)})
            print(f"[error] {mid} {peak['name']}: {exc}", file=sys.stderr)
            if args.traceback:
                import traceback

                traceback.print_exc()

        if index % args.progress == 0 or index == total or index == 1:
            elapsed = time.time() - started
            rate = index / elapsed if elapsed else 0
            eta = (total - index) / rate if rate else 0
            print(
                f"[{index}/{total}] {elapsed / 60:.1f} min · ETA {eta / 60:.1f} min · "
                f"ok {generated} · skip {skipped} · fail {len(failures)}",
                flush=True,
            )

    merge_catalog(out_dir, results)
    elapsed = time.time() - started
    size_mb = sum(m.get("bytes", 0) for m in results) / 1048576
    print(
        f"[done] {total} 座 · 生成 {generated} · 跳过 {skipped} · 失败 {len(failures)} · "
        f"{elapsed / 60:.1f} min · {size_mb:.0f} MB"
    )
    if failures:
        fail_path = out_dir / "failed_peaks.json"
        with open(fail_path, "w", encoding="utf-8") as f:
            json.dump(failures, f, ensure_ascii=False, indent=2)
        print(f"[failures] {fail_path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
