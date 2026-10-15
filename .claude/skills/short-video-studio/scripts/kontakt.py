"""Contact sheet: one row per scene with all its variants, to pick from.

Run:  uv run --with pillow python kontakt.py PROJEKT_DIR [--nur 1 2 3]
Writes PROJEKT_DIR/kontakt.jpg. Show it to the user, then set "variante" per scene in projekt.json.
"""
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
import argparse

from PIL import Image, ImageDraw

from gemeinsam import auswahl, lade, nr2

ap = argparse.ArgumentParser()
ap.add_argument("projekt")
ap.add_argument("--nur", nargs="*")
args = ap.parse_args()
d, p = lade(args.projekt)

w, h = 216, 384
zeilen = []
for s in auswahl(p, args.nur):
    fs = sorted((d / "bilder").glob(f"szene{nr2(s['nr'])}_v*.png"))
    if fs:
        zeilen.append((s["nr"], fs))
if not zeilen:
    raise SystemExit("Keine Bilder in bilder/ — erst bilder.py laufen lassen")
spalten = max(len(fs) for _, fs in zeilen)
c = Image.new("RGB", (60 + spalten * (w + 8), len(zeilen) * (h + 8)), "white")
dr = ImageDraw.Draw(c)
for r, (nr, fs) in enumerate(zeilen):
    dr.text((10, r * (h + 8) + h // 2), str(nr), fill="black")
    for k, f in enumerate(fs):
        c.paste(Image.open(f).convert("RGB").resize((w, h)), (60 + k * (w + 8), r * (h + 8)))
        dr.text((64 + k * (w + 8), r * (h + 8) + 4), f.stem.split("_")[-1], fill="yellow")
c.save(d / "kontakt.jpg", quality=85)
print(d / "kontakt.jpg")
