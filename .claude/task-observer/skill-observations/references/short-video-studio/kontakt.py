"""Kontaktbogen: je Szene eine Zeile mit allen Varianten (zum Auswählen)."""
import sys, glob, re
from PIL import Image, ImageDraw
from pathlib import Path
ordner, ziel, von, bis = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
w, h = 216, 384
zeilen = []
for nr in range(von, bis + 1):
    fs = sorted(glob.glob(f"{ordner}/szene{nr:02d}_v*.png"))
    if fs: zeilen.append((nr, fs))
c = Image.new("RGB", (60 + 3 * (w + 8), len(zeilen) * (h + 8)), "white"); d = ImageDraw.Draw(c)
for r, (nr, fs) in enumerate(zeilen):
    d.text((10, r * (h + 8) + h // 2), str(nr), fill="black")
    for k, f in enumerate(fs):
        c.paste(Image.open(f).resize((w, h)), (60 + k * (w + 8), r * (h + 8)))
        d.text((64 + k * (w + 8), r * (h + 8) + 4), f"v{k+1}", fill="yellow")
c.save(ziel, quality=85)
