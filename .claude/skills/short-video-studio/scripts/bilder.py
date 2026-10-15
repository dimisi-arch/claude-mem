"""Generate the scene images locally with SDXL-Turbo on the CPU (free, ~25 s per image on 4 cores).

Run:  uv run --index https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match \
        --with torch --with diffusers --with transformers --with accelerate python bilder.py PROJEKT_DIR [--nur 3 5] [--varianten N]
Writes PROJEKT_DIR/bilder/szeneNN_vK.png (576x1024 SDXL-Turbo or 512x896 SD-Turbo; the cut scales them up).
First run downloads the model (~7 GB) into the Hugging Face cache.
"""
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
import argparse
import time

from gemeinsam import auswahl, lade, nr2

ap = argparse.ArgumentParser()
ap.add_argument("projekt")
ap.add_argument("--nur", nargs="*", help="only these scene numbers")
ap.add_argument("--varianten", type=int, help="override variants per scene")
ap.add_argument("--schritte", type=int, default=4)
ap.add_argument("--modell", choices=["auto", "sdxl", "sd"], default="auto",
                help="sdxl = SDXL-Turbo (better, needs a CPU with bf16 support), sd = SD-Turbo (smaller, any CPU)")
args = ap.parse_args()
d, p = lade(args.projekt)

import torch  # noqa: E402 (slow import after the cheap checks)
from diffusers import AutoPipelineForText2Image  # noqa: E402

def bf16_cpu():
    try:
        flags = open("/proc/cpuinfo").read()
    except OSError:  # Windows/macOS: no cpuinfo; PCs usually lack AMX, take the safe choice
        return False
    return "amx_bf16" in flags or "avx512_bf16" in flags


modell = args.modell if args.modell != "auto" else ("sdxl" if bf16_cpu() else "sd")
if modell == "sdxl":
    # bf16 is fast only with AMX/avx512_bf16 (~25 s per image); emulated it takes ~4 min.
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.bfloat16, variant="fp16")
    W, H = 576, 1024
else:
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float32)
    W, H = 512, 896
# Memory: the cloud shell allows ~14 GB incl. file cache; SDXL with full attention overflows it.
pipe.enable_attention_slicing()
print(f"Modell: {modell} ({W}x{H})", flush=True)
tok = pipe.tokenizer
out = d / "bilder"
out.mkdir(exist_ok=True)

for s in auswahl(p, args.nur):
    # Style FIRST: CLIP reads only 77 tokens, so a style appended at the end gets cut silently.
    prompt = f"{p['stil']}, {s['bild']}" if p["stil"] else s["bild"]
    n_tok = len(tok(prompt).input_ids)
    if n_tok > 77:
        print(f"WARNUNG Szene {s['nr']}: Prompt hat {n_tok} Token, ab 77 wird abgeschnitten — kürzen")
    for v in range(args.varianten or s.get("varianten", 1)):
        t = time.time()
        img = pipe(prompt=prompt, num_inference_steps=args.schritte, guidance_scale=0.0, width=W, height=H,
                   generator=torch.Generator().manual_seed(int(s.get("seed", 1000 + 100 * int(s["nr"]))) + v)).images[0]
        f = out / f"szene{nr2(s['nr'])}_v{v + 1}.png"
        img.save(f)
        print(f"{f.name} {time.time() - t:.0f}s", flush=True)
