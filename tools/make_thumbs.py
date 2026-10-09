#!/usr/bin/env python3
"""projects.json の各プロジェクトのサムネイルを thumbs/ に生成する。

- thumbnail_source (なければ demo_url) をヘッドレス Chromium で撮影する
- 撮影に失敗したら、タイトルから生成したカード画像で代替する
- 既にファイルがある場合はスキップ。--force で撮り直し

使い方:
    pip install playwright pillow
    playwright install chromium
    python3 tools/make_thumbs.py [--force] [--only id,id,...]
"""
import argparse
import asyncio
import json
import pathlib
import sys

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "projects.json"
THUMBS = ROOT / "thumbs"
W, H = 1280, 800

FALLBACK_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{w}px;height:{h}px}}
body{{display:flex;align-items:flex-end;background:
 radial-gradient(900px 600px at 15% 10%, #52C3F1 0%, transparent 60%),
 radial-gradient(800px 600px at 90% 90%, #FDD541 0%, transparent 55%),
 #0B2A4A;font-family:"Hiragino Sans","Noto Sans JP","Noto Sans CJK JP",sans-serif;color:#fff}}
.in{{padding:72px;max-width:90%}}
.t{{font-size:64px;font-weight:800;line-height:1.15;letter-spacing:-.01em;text-wrap:balance}}
.s{{margin-top:20px;font-size:26px;opacity:.8}}
.b{{position:absolute;top:60px;left:72px;font-size:22px;letter-spacing:.2em;opacity:.7}}
</style></head><body><div class="b">HACKATSUON 2026</div>
<div class="in"><div class="t">{title}</div><div class="s">{team}</div></div></body></html>"""


async def shoot(ctx, pr, out):
    url = pr.get("thumbnail_source") or pr.get("demo_url")
    page = await ctx.new_page()
    try:
        await page.goto(url, timeout=30000, wait_until="networkidle")
        await page.wait_for_timeout(2500)
        await page.screenshot(path=str(out), type="jpeg", quality=82)
        return "shot"
    except Exception as e:  # noqa: BLE001
        print(f"  screenshot failed ({str(e)[:80]}), using fallback", file=sys.stderr)
        await page.set_content(FALLBACK_HTML.format(w=W, h=H, title=esc(pr["title"]), team=esc(pr["team"])))
        await page.screenshot(path=str(out), type="jpeg", quality=82)
        return "fallback"
    finally:
        await page.close()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


async def main(force, only):
    d = json.loads(DATA.read_text())
    THUMBS.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": W, "height": H}, locale="ja-JP")
        for pr in d["projects"]:
            if only and pr["id"] not in only:
                continue
            out = ROOT / pr.get("thumbnail", f"thumbs/{pr['id']}.jpg")
            if out.exists() and not force:
                print(f"skip {pr['id']} (exists)")
                continue
            print(f"{pr['id']}: ", end="", flush=True)
            print(await shoot(ctx, pr, out))
        await b.close()
    try:
        from PIL import Image

        for pr in d["projects"]:
            f = ROOT / pr.get("thumbnail", f"thumbs/{pr['id']}.jpg")
            if f.exists():
                im = Image.open(f)
                if im.width > 960:
                    im.resize((960, int(960 * im.height / im.width)), Image.LANCZOS).save(f, quality=82, optimize=True)
    except ImportError:
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    asyncio.run(main(a.force, set(filter(None, a.only.split(",")))))
