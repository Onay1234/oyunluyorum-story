#!/usr/bin/env python3
"""Oyunluyorum günlük indirim story'sini (1080x1920 PNG) çizer.

Kullanım: python3 render_story.py story.json cikti.png
story.json:
{
  "date": "18 Kasım",
  "subtitle": "1 ücretsiz oyun + 5 dev indirim",
  "bg_image": "/yol/arka.jpg",
  "rows": [
    {"name": "Detroit: Become Human", "store": "Epic", "old": "142,00 TL",
     "new": "28,40 TL", "cut": 80, "free": false, "until": "2 Aralık'a kadar",
     "image": "/yol/detroit.jpg"}
  ]
}
En fazla 6 satır. "free": true satırı sarı ve "Ücretsiz" yazılı çizilir.
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
LOGO = ROOT / "assets" / "logo.png"
LOGO_FULL = ROOT / "assets" / "logo-full-white.png"
BG, SURFACE, ACCENT = "#1A0630", "#2E0D52", "#FFC50D"
COND = "'Barlow Condensed', 'Arial Narrow', sans-serif"


def uri(p):
    return pathlib.Path(p).resolve().as_uri() if p else ""


def e(s):
    return html.escape(str(s or ""))


def logo_img(h):
    if LOGO.exists():
        return f'<img src="{uri(LOGO)}" alt="" style="height:{h}px;width:auto">'
    return ""


def row(r):
    name = f'<div lang="en" style="font-family:{COND};font-weight:800;font-size:40px;line-height:1.05;text-transform:uppercase">{e(r["name"])}</div>'
    if r.get("free"):
        thumb = (f'<img src="{uri(r["image"])}" style="width:200px;height:112px;flex:none;border-radius:14px;object-fit:cover;display:block">'
                 if r.get("image") else
                 f'<div style="width:200px;height:112px;flex:none;border-radius:14px;background:{BG};display:flex;align-items:center;justify-content:center">{logo_img(64)}</div>')
        return f'''<div style="display:flex;align-items:center;gap:24px;padding:18px;border-radius:24px;background:{ACCENT};color:{BG}">
{thumb}<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:6px">{name}
<div style="font-size:24px;font-weight:600">{e(r.get("store"))} · {e(r.get("until"))}</div></div>
<div style="flex:none;font-family:{COND};font-weight:800;font-size:52px;text-transform:uppercase">Ücretsiz</div></div>'''
    thumb = (f'<img src="{uri(r["image"])}" style="width:200px;height:112px;flex:none;border-radius:14px;object-fit:cover;display:block">'
             if r.get("image") else
             f'<div style="width:200px;height:112px;flex:none;border-radius:14px;background:{BG}"></div>')
    return f'''<div style="display:flex;align-items:center;gap:24px;padding:18px;border-radius:24px;background:{SURFACE}">
{thumb}<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:6px">{name}
<div style="font-size:24px;color:#C9B6E4">{e(r.get("store"))} · <span style="text-decoration:line-through">{e(r.get("old"))}</span></div></div>
<div style="flex:none;display:flex;flex-direction:column;align-items:flex-end;gap:6px">
<div style="font-family:{COND};font-weight:800;font-size:48px;line-height:1;color:{ACCENT}">{e(r.get("new"))}</div>
<div style="padding:4px 12px;border-radius:10px;background:{ACCENT};color:{BG};font-family:{COND};font-weight:800;font-size:30px">-%{e(r.get("cut"))}</div></div></div>'''


def build(d):
    rows = "\n".join(row(r) for r in d["rows"][:6])
    brand = (f'<img src="{uri(LOGO_FULL)}" alt="Oyunluyorum" style="height:60px;width:auto">' if LOGO_FULL.exists()
             else f'<div style="font-family:{COND};font-weight:800;font-size:40px;letter-spacing:4px;color:{ACCENT}">OYUNLUYORUM</div>')
    bg = (f'<div style="position:absolute;left:0;top:0;width:1080px;height:900px;overflow:hidden">'
          f'<img src="{uri(d["bg_image"])}" style="width:100%;height:100%;object-fit:cover;display:block">'
          f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,6,48,.55) 0%,rgba(26,6,48,.35) 30%,rgba(26,6,48,.85) 70%,{BG} 100%)"></div></div>'
          if d.get("bg_image") else "")
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Barlow Condensed';font-weight:800;src:url("{uri(FONTS/'BarlowCondensed-ExtraBold.ttf')}")}}
@font-face{{font-family:'Inter';font-weight:100 900;src:url("{uri(FONTS/'Inter.ttf')}")}}
body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1920px;box-sizing:border-box;background:{BG};color:#fff;font-family:Inter,Arial,sans-serif;display:flex;flex-direction:column;padding:150px 72px 170px;gap:40px;position:relative;overflow:hidden">
{bg}
<div style="position:relative;display:flex;justify-content:space-between;align-items:center;gap:24px">
{brand}
<div style="font-size:28px;font-weight:600;color:#EDE4F7">{e(d["date"])}</div></div>
<div style="position:relative;display:flex;flex-direction:column;gap:20px;margin-top:60px">
<h1 style="margin:0;font-family:{COND};font-weight:800;font-size:150px;line-height:.98;text-transform:uppercase;text-shadow:0 4px 24px rgba(0,0,0,.6)">Günün<br><span style="color:{ACCENT}">indirimleri</span></h1>
<p style="margin:0;font-size:34px;line-height:1.35;color:#EDE4F7">{e(d.get("subtitle"))}</p></div>
<div style="position:relative;display:flex;flex-direction:column;gap:18px;margin-top:auto">
{rows}</div>
<div style="position:relative;display:flex;justify-content:flex-end;align-items:center">
<div style="font-size:28px;color:#C9B6E4">@oyunlu_yorum</div></div>
</div></body></html>'''


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    out = pathlib.Path(sys.argv[2]).resolve()
    page_file = out.with_suffix(".html")
    page_file.write_text(build(d), encoding="utf-8")
    import shutil
    exe = shutil.which("google-chrome") or shutil.which("chromium")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(page_file.as_uri())
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(out), type="png")
        b.close()
    page_file.unlink()


if __name__ == "__main__":
    main()
