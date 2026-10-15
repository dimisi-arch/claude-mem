"""Speak every scene's text into PROJEKT_DIR/ton/zNN.wav.

Run:  uv run --with edge-tts --with requests python stimme.py PROJEKT_DIR [--engine auto|fish|edge|piper] [--nur 2 5]

Engines, in the order "auto" tries them:
  fish   Fish Audio API (best quality; the voice for the videos). Needs FISH_API_KEY in the
         environment and stimme.fish_voice (a voice model id) in projekt.json.
  edge   Microsoft neural voice (free, online). Answers 403 from some cloud IPs, on and off.
  piper  Offline voice (free). Plainer sound; downloads the voice once (~114 MB).
The engine actually used per line is printed and written to ton/engine.txt.
"""
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
import argparse
import asyncio
import os
import re
import subprocess
import tempfile
from pathlib import Path

from gemeinsam import auswahl, lade, nr2, sh, tonpfad

PIPER_DIR = Path.home() / ".cache" / "vorlesen" / "piper"
PIPER = ["uv", "run", "-q", "--with", "piper-tts", "python", "-m"]


def ausgesprochen(text, aussprache):
    for wort, laut in sorted(aussprache.items(), key=lambda kv: -len(kv[0])):
        text = re.sub(rf"\b{re.escape(wort)}\b", laut, text, flags=re.IGNORECASE)
    return text


def fish(text, ziel, st):
    import requests

    key = os.environ.get("FISH_API_KEY", "")
    if not key or not st["fish_voice"]:
        raise RuntimeError("FISH_API_KEY oder stimme.fish_voice fehlt")
    r = requests.post("https://api.fish.audio/v1/tts", timeout=120,
                      headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                               "model": st["fish_model"]},
                      json={"text": text, "reference_id": st["fish_voice"], "format": "wav",
                            "prosody": {"speed": st["tempo"], "normalize_loudness": True}})
    if r.status_code != 200:
        raise RuntimeError(f"Fish Audio {r.status_code}: {r.text[:200]}")
    Path(ziel).write_bytes(r.content)


def edge(text, ziel, st):
    import certifi

    if os.environ.get("SSL_CERT_FILE"):  # cloud: the HTTPS proxy has its own CA
        certifi.where = lambda: os.environ["SSL_CERT_FILE"]
    import edge_tts

    with tempfile.TemporaryDirectory() as tmp:
        mp3 = os.path.join(tmp, "a.mp3")
        com = edge_tts.Communicate(text, st["edge_voice"], rate=st["edge_rate"], pitch=st["edge_pitch"])
        asyncio.run(asyncio.wait_for(com.save(mp3), timeout=90))
        sh("ffmpeg", "-v", "error", "-y", "-i", mp3, "-ar", "44100", "-ac", "1", str(ziel))


def piper(text, ziel, st):
    model = PIPER_DIR / f"{st['piper_voice']}.onnx"
    if not model.is_file():
        PIPER_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run(PIPER + ["piper.download_voices", "--download-dir", str(PIPER_DIR), st["piper_voice"]],
                       check=True, capture_output=True)
    subprocess.run(PIPER + ["piper", "-m", str(model), "-f", str(ziel), "--length-scale", f"{1 / st['tempo']:.2f}",
                            "--sentence-silence", "0.3"], input=text.encode("utf-8"), check=True, capture_output=True)


ENGINES = {"fish": fish, "edge": edge, "piper": piper}

ap = argparse.ArgumentParser()
ap.add_argument("projekt")
ap.add_argument("--engine", choices=["auto", *ENGINES])
ap.add_argument("--nur", nargs="*")
args = ap.parse_args()
d, p = lade(args.projekt)
st = p["stimme"]
wahl = args.engine or st["engine"]
reihe = ["fish", "edge", "piper"] if wahl == "auto" else [wahl]
(d / "ton").mkdir(exist_ok=True)
benutzt = {}
for s in auswahl(p, args.nur):
    text = ausgesprochen(s["text"], p["aussprache"])
    ziel = tonpfad(d, s)
    fehler = []
    for e in reihe:
        try:
            ENGINES[e](text, ziel, st)
            benutzt[s["nr"]] = e
            print(f"z{nr2(s['nr'])}.wav  {e}", flush=True)
            break
        except Exception as ex:  # try the next engine
            fehler.append(f"{e}: {type(ex).__name__} {str(ex)[:120]}")
    else:
        raise SystemExit(f"Szene {s['nr']}: keine Stimme ging — " + " | ".join(fehler))
    if fehler and wahl == "auto":
        print("   übersprungen: " + " | ".join(fehler))
if len(set(benutzt.values())) > 1:
    print("WARNUNG: gemischte Stimmen in einer Folge — mit --engine eine Stimme für alle erzwingen")
(d / "ton" / "engine.txt").write_text("".join(f"{nr2(k)} {v}\n" for k, v in sorted(benutzt.items())))
