---
name: short-video-studio
description: "Internal skill for this repo. Produce a faceless vertical short (TikTok, YouTube Shorts, Reels; 9:16, about 30-90 s) end to end: story text per scene, AI scene images (local SDXL-Turbo or SD-Turbo, free), narration (Fish Audio for videos, Microsoft or offline Piper as fallback), a pronunciation check, subtitles from the script, Ken Burns motion, sound bed, final MP4 plus check frames. Use when the user wants a story short, a Kurzvideo, a TikTok or Shorts episode, or asks Claude to act as the whole video studio. Not for code-built animations or explainers made of typography and charts (use hyperframes) or for finding historical images (historical-images)."
requires:
  - binary: ffmpeg
  - binary: ffprobe
  - binary: uv
---

# Short-video studio (internal)

One project folder per episode, one `projekt.json` that holds everything that is
episode-specific (scene prompts, narration, highlight words, title, end card,
voice). The scripts in `scripts/` read only that file, so the next episode starts
from a copy of `examples/projekt.json`, not from edited code.

Run every script from this skill's `scripts/` folder (they import `gemeinsam.py`).
The user is not a developer: report each finished stage in one German line and
show the result (contact sheet, MP3, MP4) instead of describing it.

## Pipeline

| # | Step | Command (in `scripts/`) | Time on 4 CPUs |
|---|---|---|---|
| 1 | Write story + `projekt.json` | — | — |
| 2 | Images, 2-3 variants per scene | `uv run --index https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match --with torch --with diffusers --with transformers --with accelerate python bilder.py P` (CPU torch: without the index uv pulls the multi-GB GPU build) | SDXL ~25 s per image on a bf16 CPU; SD-Turbo ~60 s elsewhere; first run downloads the model |
| 3 | Contact sheet, user picks | `uv run --with pillow python kontakt.py P` → set `"variante"` per scene | seconds |
| 4 | Narration | `uv run --with edge-tts --with requests python stimme.py P` | ~2 s per line |
| 5 | Pronunciation check | `uv run --with faster-whisper python pruefen.py P` | ~5 s per line |
| 6 | Cut | `python schnitt.py P` | ~1-2 min per minute of video |
| 7 | Look check | open `P/qa/frame_*.jpg`, send `P/folge.mp4` | — |

`P` is the project folder. Keep projects out of this public repo (scratchpad, or the
channel's private repo); only the method lives here.

## 1 — Story and project file

- Copy `examples/projekt.json`. Per scene: `bild` (English image prompt), `text`
  (German narration, numbers written as words, one or two sentences), `varianten`, `seed`,
  optional `glocke`, later `variante` (the picked image) or `datei` (any image path).
- `stil` is put in FRONT of every prompt. Keep `stil` + `bild` under 77 tokens: the image
  model cuts the rest silently; `bilder.py` warns when a prompt is too long.
- `akzent`: words shown in the highlight colour. `anzeige`: how a word appears on screen
  (`"dreizehn": "13"`). `aussprache`: respellings for the voice only (`"Zuchthaus": "Zucht-Haus"`).
- `kopfzeile` (small title in scene 1) and `abspann` (end card lines, last one highlighted) are optional.
- Keep a recurring character identical in every prompt (same clothes, hair, age words).

## 2-3 — Images

- Default: local, zero cost. `--modell auto` picks SDXL-Turbo (576x1024, clearly better) when the CPU has
  bf16 support (AMX/avx512_bf16), else SD-Turbo (512x896, engraving-like but fine). SDXL without bf16
  hardware takes ~4 min per image; force it with `--modell sdxl` only when time does not matter.
  Memory: the cloud shell is capped near 14 GB including file cache; never run two image jobs at once.
- Paid alternatives only when the user wants them: Runway image generation (returns full-size files; the free plan has images only, no video),
  Canva returns only a small preview via the tool — not usable as a frame.
- Long runs go in the background with a pid file, and are waited on by that pid:
  `nohup … > P/bilder.log 2>&1 & echo $! > P/bilder.pid`, check with `kill -0 "$(cat P/bilder.pid)"`.
  Never `pgrep -f` / `pkill -f` on the script name: the waiting shell's own command line
  matches, so the loop never ends or kills itself (happened twice).
- Do not run `pruefen.py` or other heavy CPU jobs while images render (3x slower).
- What the model cannot draw (e.g. light under a door, text on a sign) is composited on an
  existing frame with PIL rather than re-rolled ten times.

## 4-5 — Voice

`stimme.py` tries the engines in this order (`"engine": "auto"`), and prints the one used:

1. **Fish Audio** — the voice for the videos (user's decision 2026-10-15). Needs `FISH_API_KEY`
   in the environment and `stimme.fish_voice` = a voice model id from fish.audio. The API answers
   from cloud sessions. Free tier: header model `s2.1-pro-free` (default).
2. **Microsoft** (`edge_voice`, default `de-DE-ConradNeural`, rate −6 %, pitch −5 Hz: calm and deep).
   Free; answers 403 from some cloud IPs, on and off.
3. **Piper** (`de_DE-thorsten-high`), offline. Sounds plainer; pitch-shifting it made it
   "rauschig" — prefer Microsoft or Fish for a deeper voice instead of filters.

All lines of one episode must use the same engine: `stimme.py` warns on a mix — rerun with
`--engine fish|edge|piper`. Then run `pruefen.py`: every deviation is either a mispronunciation
(add to `aussprache`, rerun `stimme.py --nur N`, check again) or a Whisper spelling quirk (leave
it). Clean = exit code 0.

## 6-7 — Cut and check

- `schnitt.py` builds subtitles from the scene **text**, never from the transcript, so voice
  slips never reach the screen; 3 words at a time, no two subtitles overlap.
- Video is capped at 5 Mbit/s: film grain or noise filters otherwise blow a 1-minute short
  past 100 MB.
- Before sending, look at `qa/frame_anfang.jpg`, `frame_mitte.jpg`, `frame_ende.jpg`: subtitle
  inside the safe area, nothing cut off, highlight colour visible. Then send the MP4 with
  `SendUserFile` and one line: length, size, voice used.

## Pre-flight before sending

- [ ] Every prompt under 77 tokens (no warning from `bilder.py`)
- [ ] One voice engine for all lines; `pruefen.py` exit code 0
- [ ] `qa/` frames checked
- [ ] File size reasonable (< 30 MB per minute)
- [ ] Projekt files outside the public repo
