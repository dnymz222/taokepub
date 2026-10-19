#!/usr/bin/env python3
"""Static server + peak routes for the WebGL terrain viewers.

Routes:
    /                              tile viewer (the original N30E120 demo)
    /mountain/terrain/<ID>         peak viewer, e.g. /mountain/terrain/C327
                                   (no public peak list; direct ID only)
    /data/mountains/<ID>/...       generated heightmap + metadata
    /data/...                      tile assets

Usage:
    python3 server.py                     # http://127.0.0.1:8000/
    python3 server.py --port 8765
"""

from __future__ import annotations

import argparse
import html
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
MOUNTAINS = ROOT / "data" / "mountains"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

CATALOG_STYLE = "/css/style.css"
MOUNTAIN_STYLE = "/css/mountain.css"


def page_shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{CATALOG_STYLE}">
<link rel="stylesheet" href="{MOUNTAIN_STYLE}">
</head>
<body class="catalog-body">
{body}
</body>
</html>"""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        # Local dev server: never let regenerated assets / edited CSS go stale.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = unquote(urlparse(self.path).path)
        if path in ("/mountain", "/mountain/"):
            self.send_response(302)
            self.send_header("Location", "/mountain/terrain")
            self.end_headers()
            return
        if path in ("/mountain/terrain", "/mountain/terrain/"):
            self._not_found("请使用包含山峰 ID 的地址打开页面。")
            return
        if path.startswith("/mountain/terrain/"):
            rest = path[len("/mountain/terrain/") :].strip("/")
            if not ID_RE.fullmatch(rest):
                self._not_found("无效的山峰 ID。")
                return
            if not (MOUNTAINS / rest / "meta.json").exists():
                self._not_found(
                    f"尚未生成山峰 {html.escape(rest)} 的地形数据。"
                )
                return
            self._send_file(ROOT / "mountain.html", "text/html; charset=utf-8")
            return
        super().do_GET()

    def _send_file(self, path: Path, content_type: str) -> None:
        try:
            data = path.read_bytes()
        except OSError:
            self.send_error(500, "file not readable")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_html(self, body: str, status: int = 200) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _not_found(self, message: str) -> None:
        body = page_shell(
            "页面不存在",
            f"""<main class="catalog">
  <div class="catalog-top">
    <a href="/">← 返回地形</a>
    <span>404</span>
  </div>
  <header class="catalog-head">
    <div class="eyebrow"><span class="pulse"></span>PAGE NOT FOUND</div>
    <h1>页面不存在</h1>
    <p>{message}</p>
    <p>请通过 <code>/mountain/terrain/&lt;ID&gt;</code> 打开已生成的山峰。</p>
  </header>
</main>""",
        )
        self._send_html(body, status=404)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.bind, args.port), Handler)
    server.daemon_threads = True
    print(f"Terrain server: http://{args.bind}:{args.port}/")
    print(f"Peak pages:      http://{args.bind}:{args.port}/mountain/terrain/<ID>")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
