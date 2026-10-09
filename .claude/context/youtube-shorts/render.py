"""Render Short 1 "Ich heisse Niemand" as 1080x1920 frames piped into ffmpeg.

Usage: python3 render.py <workdir> <out.mp4>
Expects in workdir: title.png end.png x_1c94.png felsen_47abaccc.png wein.png
schatten.png nacht.png, plus video-only output; audio is muxed separately.
"""
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

D = sys.argv[1]
OUT = sys.argv[2]
W, H, FPS = 1080, 1920, 30
XF = 0.35  # crossfade seconds

def load(name):
    im = Image.open(f"{D}/{name}").convert("RGB")
    if im.size != (W, H):  # illustrations: upscale once, sharpen lightly
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
    return im

def ease(p):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, p)))

import json
TL = json.load(open(f"{D}/timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
P = {p["key"]: p for p in TL["pieces"]}
LIST_AT = P["n7"]["subs"][1][0]
# (start, end, image, (cx0, cy0, z0), (cx1, cy1, z1), shake)
SEGMENTS = [
    (0.00, P["n1"]["start"], "title.png", (0.5, 0.5, 1.00), (0.5, 0.5, 1.06), False),
    (P["n1"]["start"], P["n2"]["start"], "x_1c94.png", (0.62, 0.66, 2.0), (0.5, 0.5, 1.0), False),
    (P["n2"]["start"], P["n3"]["start"], "felsen_fix.png", (0.72, 0.5, 1.0), (0.24, 0.5, 1.0), False),
    (P["n3"]["start"], P["n5"]["start"], "wein_fix.png", (0.5, 0.5, 1.0), (0.5, 0.38, 1.3), False),
    (P["n5"]["start"], P["nb"]["start"], "schatten.png", (0.5, 0.5, 1.08), (0.5, 0.45, 1.18), True),
    (P["nb"]["start"], P["poly"]["start"], "nacht.png", (0.5, 0.42, 1.35), (0.5, 0.45, 1.2), False),
    (P["poly"]["start"], P["n7"]["start"], "schatten.png", (0.5, 0.42, 1.25), (0.5, 0.40, 1.32), True),
    (P["n7"]["start"], LIST_AT, "nacht.png", (0.5, 0.45, 1.2), (0.5, 0.5, 1.0), False),
    (LIST_AT, P["end1"]["start"], "title.png", (0.5, 0.5, 1.00), (0.5, 0.5, 1.06), False),
    (P["end1"]["start"], P["end2"]["start"], "nacht.png", (0.5, 0.80, 1.5), (0.5, 0.85, 1.75), False),
    (P["end2"]["start"], TOTAL, "end.png", (0.5, 0.5, 1.00), (0.5, 0.5, 1.04), False),
]
# (start, end, text, speaker label or None); hold each subtitle up to the next one
SUBS = []
for p in TL["pieces"]:
    for s0, s1, text in p["subs"]:
        SUBS.append([s0, s1, text, None if p["speaker"] == "Erzähler" else p["speaker"].upper()])
for i in range(len(SUBS) - 1):
    SUBS[i][1] = min(SUBS[i + 1][0], SUBS[i][1] + 0.35)
SUBS[-1][1] = TOTAL

IMAGES = {name: load(name) for name in {s[2] for s in SEGMENTS}}
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
WHITE, GOLD = (255, 255, 255), (240, 190, 95)
SUB_CY, SUB_MAXW = 1260, 860
LABEL_FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)

def view(img, cx, cy, zoom, dx=0.0, dy=0.0):
    iw, ih = img.size
    ww = min(iw, ih * 9 / 16) / zoom
    wh = ww * 16 / 9
    x0 = min(max(cx * iw - ww / 2 + dx * iw, 0), iw - ww)
    y0 = min(max(cy * ih - wh / 2 + dy * ih, 0), ih - wh)
    s = ww / W
    return img.transform((W, H), Image.AFFINE, (s, 0, x0, 0, s, y0), resample=Image.BICUBIC)

def segment_frame(seg, t):
    start, end, name, a, b, shake = seg
    p = ease((t - start) / (end - start))
    cx, cy, z = (a[i] + (b[i] - a[i]) * p for i in range(3))
    dx = dy = 0.0
    if shake:
        dx = 0.004 * math.sin(t * 9.0)
        dy = 0.003 * math.sin(t * 7.3 + 1.0)
    return view(IMAGES[name], cx, cy, z, dx, dy)

def wrap(words):
    lines, cur = [], []
    for w in words:
        trial = " ".join(cur + [w])
        if cur and FONT.getlength(trial) > SUB_MAXW:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines

def draw_sub(frame, text, label=None):
    d = ImageDraw.Draw(frame)
    lines = wrap(text.split())
    lh = 78
    y = SUB_CY - lh * (len(lines) - 1) / 2
    if label:
        d.text((W / 2, y - 70), label, font=LABEL_FONT, fill=(200, 180, 150), anchor="mm",
               stroke_width=4, stroke_fill=(0, 0, 0))
    space = FONT.getlength(" ")
    for line in lines:
        x = W / 2 - FONT.getlength(" ".join(line)) / 2
        for w in line:
            color = GOLD if "Niemand" in w else WHITE
            d.text((x, y), w, font=FONT, fill=color, anchor="lm",
                   stroke_width=6, stroke_fill=(0, 0, 0))
            x += FONT.getlength(w) + space
        y += lh

_yy, _xx = np.mgrid[0:H, 0:W]
_r = np.sqrt(((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2)
VIGNETTE = np.clip(1.0 - 0.38 * np.clip(_r - 0.55, 0, None) ** 1.6, 0.55, 1.0)[..., None].astype(np.float32)
_rng = np.random.default_rng(7)
GRAIN = [_rng.normal(0, 3.0, (H, W, 1)).astype(np.float32)]  # static paper-like texture: survives YouTube compression

def finish(im, t):
    a = np.asarray(im, dtype=np.float32) * VIGNETTE  # no grain: it costs bitrate and YouTube smears it
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def frame_at(t):
    idx = max(i for i, s in enumerate(SEGMENTS) if s[0] <= t)
    cur = segment_frame(SEGMENTS[idx], t)
    if idx > 0 and t - SEGMENTS[idx][0] < XF:
        prev = segment_frame(SEGMENTS[idx - 1], t)
        cur = Image.blend(prev, cur, (t - SEGMENTS[idx][0]) / XF)
    cur = finish(cur, t)
    for s0, s1, text, label in SUBS:
        if s0 <= t < s1:
            draw_sub(cur, text, label)
            break
    # fade in from black at the very start, fade out at the end
    fade = min(1.0, t / 0.4, (TOTAL - t) / 0.8)
    if fade < 1.0:
        cur = Image.blend(Image.new("RGB", (W, H)), cur, max(0.0, fade))
    return cur

def main():
    n = int(TOTAL * FPS)
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
        "-crf", "18", "-pix_fmt", "yuv420p", OUT,
    ], stdin=subprocess.PIPE)
    for i in range(n):
        ff.stdin.write(frame_at(i / FPS).tobytes())
    ff.stdin.close()
    sys.exit(ff.wait())

if __name__ == "__main__":
    main()
