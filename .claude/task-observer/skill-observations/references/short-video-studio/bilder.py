"""Erzeugt Szenenbilder lokal mit SDXL-Turbo auf der CPU.
Aufruf: python bilder.py szenen.json ausgabeordner [nur_nummer]"""
import json, sys, time, torch
from pathlib import Path
from diffusers import AutoPipelineForText2Image

STIL = "oil painting, muted sepia and grey tones, film grain, dramatic light, cinematic"
torch.set_num_threads(4)
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.bfloat16, variant="fp16")
szenen = json.load(open(sys.argv[1]))
out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
nur = sys.argv[3:] 
for s in szenen:
    if nur and str(s["nr"]) not in nur: continue
    for v in range(s.get("varianten", 1)):
        t = time.time()
        img = pipe(prompt=f'{s["prompt"]}, {STIL}', num_inference_steps=4, guidance_scale=0.0,
                   width=576, height=1024, generator=torch.Generator().manual_seed(s.get("seed", 1000) + v)).images[0]
        p = out / f'szene{s["nr"]:02d}_v{v+1}.png'; img.save(p)
        print(f'{p.name} {time.time()-t:.0f}s', flush=True)
