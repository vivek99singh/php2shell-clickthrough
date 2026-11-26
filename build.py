#!/usr/bin/env python3
"""Build a single-file click-through from shots.json + screens/.

Usage:
  python3 build.py                      # writes click-through.html
  python3 build.py --title "My demo"    # title shown in the tab and the header
  python3 build.py --out other.html     # different output file

Settings can also live in deck.json next to this file: {"title": "...", "out": "..."}.
Missing screens become placeholders, so you can build before every picture exists.
hotspot = [left, top, width, height] in percent of the screenshot; null = no hotspot.
"""
import argparse, base64, html, io, json, pathlib, shutil, subprocess, tempfile

root = pathlib.Path(__file__).resolve().parent
cfg = json.loads((root / "deck.json").read_text()) if (root / "deck.json").exists() else {}
ap = argparse.ArgumentParser()
ap.add_argument("--title", default=cfg.get("title", "Click-through"))
ap.add_argument("--out", default=cfg.get("out", "click-through.html"))
ap.add_argument("--fragment", action="store_true", help="leave out <!doctype>/<html> (for hosts that wrap the page)")
ap.add_argument("--max-width", type=int, default=cfg.get("max_width", 2000), help="shrink wider screenshots to this width")
a = ap.parse_args()

def to_jpeg(f: pathlib.Path) -> bytes:
    """JPEG bytes (quality 93), resized to max-width. Uses Pillow, else macOS sips, else the file as it is."""
    try:
        from PIL import Image
        im = Image.open(f).convert("RGB")
        if im.width > a.max_width:
            im = im.resize((a.max_width, round(im.height * a.max_width / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=93); return b.getvalue()
    except ImportError:
        pass
    if shutil.which("sips"):
        with tempfile.TemporaryDirectory() as t:
            o = pathlib.Path(t) / "o.jpg"
            w = int(subprocess.run(["sips", "-g", "pixelWidth", f], capture_output=True, text=True).stdout.split()[-1])
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "93"] + (["--resampleWidth", str(a.max_width)] if w > a.max_width else []) + [f, "--out", o], check=True, capture_output=True)
            return o.read_bytes()
    return f.read_bytes()

shots = json.loads((root / "shots.json").read_text())
missing = []
for s in shots:
    f = next((p for e in ("png", "jpg", "jpeg") if (p := root / "screens" / f"{s['id']}.{e}").exists()), None)
    if not f:
        missing.append(s["id"]); s["img"] = None; continue
    data = to_jpeg(f)
    mime = "image/jpeg" if data[:2] == b"\xff\xd8" else "image/png"
    s["img"] = f"data:{mime};base64," + base64.b64encode(data).decode()

page = (root / "player.html").read_text()
page = page.replace("/*TITLE*/", html.escape(a.title)).replace('/*TITLEJS*/""', json.dumps(a.title))
page = page.replace("/*SHOTS*/[]", json.dumps(shots).replace("</", "<\\/"))
if a.fragment:
    page = page.replace('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', "").replace("</script></html>", "</script>")
out = pathlib.Path(a.out) if pathlib.Path(a.out).is_absolute() else root / a.out
out.write_text(page)
size = out.stat().st_size / 1e6
print(f"{a.out}: {len(shots)-len(missing)} of {len(shots)} screens in place, {size:.1f} MB")
if missing: print("missing:", ", ".join(missing))
