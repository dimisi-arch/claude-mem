"""Build src/<part>/captions.json from a voice track and its timeline.

Whisper (faster-whisper, runs on CPU or GPU) gives each spoken word a start
time; the words are matched one by one against the script in timeline.json,
so the captions always show the script's spelling.

Usage:
  pip install faster-whisper numpy
  python3 tools/captions.py voice.wav timeline.json src/teil1/captions.json [--device cuda]

timeline.json comes from the voice assembly step (.claude/context/youtube-shorts/assemble.py).
"""
import json
import re
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

voice, timeline_path, out_path = sys.argv[1:4]
device = "cuda" if "--device" in sys.argv and sys.argv[sys.argv.index("--device") + 1] == "cuda" else "cpu"

raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", voice, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
model = WhisperModel("medium", device=device, compute_type="float16" if device == "cuda" else "int8")
segments, _ = model.transcribe(np.frombuffer(raw, np.float32), language="de", word_timestamps=True, beam_size=5)
heard = [w for s in segments for w in s.words]

def norm(s):
    return re.sub(r"[^\wäöüß]", "", s.lower())

tl = json.load(open(timeline_path, encoding="utf-8"))
pages, i = [], 0
for p in tl["pieces"]:
    for s0, s1, text in p["subs"]:
        words = []
        for token in text.split():
            w = heard[i]
            if norm(w.word) != norm(token):
                sys.exit(f"mismatch at word {i}: heard {w.word!r}, script {token!r} - check the voice take")
            i += 1
            start = min(max(w.start, p["start"]), p["end"] - 0.05)
            words.append({"text": token, "startMs": round(start * 1000), "key": "niemand" in norm(token)})
        for k, w in enumerate(words):
            w["endMs"] = words[k + 1]["startMs"] if k + 1 < len(words) else round(min(p["end"], s1 + 0.25) * 1000)
        pages.append({"startMs": words[0]["startMs"], "endMs": words[-1]["endMs"],
                      "speaker": None if p["speaker"] == "Erzähler" else p["speaker"].upper(), "words": words})
if i != len(heard):
    sys.exit(f"script has {i} words, Whisper heard {len(heard)}")
for k in range(len(pages) - 1):  # hold a line until the next starts, at most 400 ms
    pages[k]["endMs"] = min(pages[k + 1]["startMs"], pages[k]["endMs"] + 400)
pages[-1]["endMs"] = round(tl["total"] * 1000)

json.dump({"totalMs": round(tl["total"] * 1000),
           "pieces": [{k: p[k] for k in ("key", "start", "end", "speaker")} for p in tl["pieces"]],
           "pages": pages}, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pages)} caption lines, {i} words -> {out_path}")
