"""Title and end cards for an "Age of Geschichte" Short (1080x1920).

Usage: python3 cards.py <workdir> <series> <part> <keyword> <subline> <logo.png>
e.g.   python3 cards.py work "DIE ODYSSEE" 1 NIEMAND "Οὖτις · Outis" Profilbild.png
Writes title.png and end.png ("TEIL <part+1> FOLGT") into workdir.
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

D, SERIES, PART, KEY, SUB, LOGO = sys.argv[1:7]
W, H = 1080, 1920
GOLD = (232, 180, 90)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def base():
    im = Image.new("RGBA", (W, H), (8, 6, 5, 255))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((140, 560, 940, 1360), fill=(120, 60, 20, 90))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))
    return im

def fit(text, path, size, maxw):
    font = ImageFont.truetype(path, size)
    while font.getlength(text) > maxw:
        size -= 4
        font = ImageFont.truetype(path, size)
    return font

def glow_text(im, xy, text, font):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=GOLD + (255,), anchor="mm")
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(18)))
    im.alpha_composite(layer)

im = base()
d = ImageDraw.Draw(im)
d.text((W // 2, 770), f"{SERIES}  ·  TEIL {PART}", font=ImageFont.truetype(REG, 46), fill=(200, 180, 150, 255), anchor="mm")
glow_text(im, (W // 2, 900), KEY, fit(KEY, BOLD, 190, 860))
ImageDraw.Draw(im).text((W // 2, 1050), SUB, font=ImageFont.truetype(REG, 64), fill=(200, 180, 150, 255), anchor="mm")
im.convert("RGB").save(f"{D}/title.png")

im = base()
glow_text(im, (W // 2, 330), f"TEIL {int(PART) + 1} FOLGT", fit(f"TEIL {int(PART) + 1} FOLGT", BOLD, 96, 900))
logo = Image.open(LOGO).convert("RGBA").resize((480, 480))
mask = Image.new("L", (480, 480), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 479, 479), fill=255)
im.paste(logo, (300, 460), mask)
d = ImageDraw.Draw(im)
d.text((W // 2, 1030), "Age of Geschichte", font=ImageFont.truetype(BOLD, 82), fill=(245, 235, 215, 255), anchor="mm")
d.text((W // 2, 1110), "Mythen. Legenden. Was wirklich geschah.", font=ImageFont.truetype(REG, 44), fill=(200, 180, 150, 255), anchor="mm")
im.convert("RGB").save(f"{D}/end.png")
