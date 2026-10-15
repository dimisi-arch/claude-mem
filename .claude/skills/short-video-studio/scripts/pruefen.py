"""Check the narration by ear-proxy: Whisper transcribes every ton/zNN.wav, a word diff against the
scene text shows the words the voice got wrong.

Run:  uv run --with faster-whisper python pruefen.py PROJEKT_DIR [--nur 2 5]
Exit code = number of scenes with deviations (0 = clean). Fix a mispronounced word by adding a
respelling to "aussprache" in projekt.json, rerun stimme.py --nur N, then this check again.
Do not run it in parallel with bilder.py: both are CPU-bound and slow each other down 3x.
"""
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
import argparse
import difflib
import re
import subprocess

import numpy as np
from faster_whisper import WhisperModel

from gemeinsam import auswahl, lade, nr2, tonpfad

ap = argparse.ArgumentParser()
ap.add_argument("projekt")
ap.add_argument("--nur", nargs="*")
args = ap.parse_args()
d, p = lade(args.projekt)


def woerter(t):
    return re.findall(r"[a-zäöüß0-9]+", t.lower())


m = WhisperModel("small", device="cpu", compute_type="int8")
schlecht = 0
for s in auswahl(p, args.nur):
    f = tonpfad(d, s)
    if not f.is_file():
        print(f"z{nr2(s['nr'])}: fehlt — erst stimme.py")
        schlecht += 1
        continue
    # Decode with ffmpeg: faster-whisper's own file reader breaks on some PyAV versions.
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    gehoert = woerter(" ".join(x.text for x in m.transcribe(a, language="de", beam_size=5)[0]))
    soll = woerter(s["text"])
    diffs = []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, soll, gehoert, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        w, g = " ".join(soll[a1:a2]), " ".join(gehoert[b1:b2])
        if any(c.isdigit() for c in w + g):  # Whisper writes numbers as digits
            continue
        diffs.append(f"{w or '—'} → {g or '—'}")
    if diffs:
        schlecht += 1
        print(f"z{nr2(s['nr'])}: " + "; ".join(diffs))
    else:
        print(f"z{nr2(s['nr'])}: sauber")
print(f"{schlecht} Szene(n) mit Abweichungen")
raise SystemExit(schlecht)
