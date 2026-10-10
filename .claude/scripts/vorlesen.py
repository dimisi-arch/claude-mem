"""Turn a German text file into an MP3 voice message (the user's chat summaries).

Run:   uv run --with edge-tts python .claude/scripts/vorlesen.py TEXT.txt OUT.mp3
Check: uv run --with edge-tts --with faster-whisper python .claude/scripts/vorlesen.py TEXT.txt OUT.mp3 --check

Every message is checked before it is sent (standing rule): --check transcribes the audio
with Whisper, lists words that came out differently from the text, and reports the pauses.
Fix a mispronounced English name by adding it to PRONUNCIATION, then run again until the
check is clean. Default voice: de-DE-FlorianMultilingualNeural (male; the user likes its
pitch). Uses Microsoft's free online voices, so it needs internet; needs ffmpeg.

Write the text as flowing spoken German: longer connected sentences, no lists, links,
brackets, abbreviations or digits (write numbers as words).
"""

import argparse
import asyncio
import difflib
import os
import re
import subprocess
import tempfile

import certifi

# Cloud containers route HTTPS through a proxy with its own CA; edge-tts only trusts certifi.
if os.environ.get("SSL_CERT_FILE"):
    certifi.where = lambda: os.environ["SSL_CERT_FILE"]

import edge_tts  # noqa: E402 (must follow the certifi patch)

VOICE = "de-DE-FlorianMultilingualNeural"

# English names the German voice gets wrong, respelled so it says them right. Each entry was
# found with --check (Whisper heard the original spelling as something else).
# 2026-10-10: "Claude" came out as "Cloud", "GitHub" as "Getub". Agent Reach, Headroom,
# Anthropic, Notion and Setup were already correct. Longer names first: "Find Skills" before "Find".
PRONUNCIATION = {
    "Claude": "Clawd",
    "GitHub": "Git Hub",
    "Impeccable": "Im-peckable",  # was heard as "Impact Käbel"
    "Make": "Mehk",  # the automation service, was heard as "Meg"
    "Find Skills": "Feind Skills",  # was heard as "Fine" / "Fame"
    "Dashboards": "Dashbords",
    "Dashboard": "Dashbord",
}

# Pauses longer than this are cut down to it. Measured 2026-10-10: 19 % of a message was
# silence, 17 pauses over 0.5 s — that is what the user heard as "abgehackt".
MAX_PAUSE = 0.3


def prepare(text: str) -> str:
    for word, spoken in PRONUNCIATION.items():
        text = re.sub(rf"\b{re.escape(word)}\b", spoken, text)
    # Hard line breaks inside a paragraph make the voice pause mid-sentence.
    paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text)]
    return "\n\n".join(p for p in paragraphs if p)


def tighten_pauses(src: str, dst: str) -> None:
    """Cut every quiet stretch longer than MAX_PAUSE down to MAX_PAUSE (frame-wise RMS)."""
    import numpy as np

    sr = 24000
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-f", "s16le", "-ac", "1",
                          "-ar", str(sr), "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32)
    hop = sr // 100  # 10 ms frames
    n = len(a) // hop
    rms = np.sqrt((a[: n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-9)
    quiet = 20 * np.log10(rms / 32768) < -40
    keep = np.ones(n, bool)
    limit = int(MAX_PAUSE * 100)
    i = 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if j - i > limit:  # keep the first and last half of the allowed pause
                keep[i + limit // 2 : j - (limit - limit // 2)] = False
            i = j
        else:
            i += 1
    out = np.concatenate([a[k * hop : (k + 1) * hop] for k in range(n) if keep[k]] + [a[n * hop :]])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(sr),
                    "-i", "-", "-b:a", "96k", dst], input=out.astype(np.int16).tobytes(), check=True)


def pause_stats(path: str) -> str:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                          "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    pauses = [float(x) for x in re.findall(r"silence_duration: ([0-9.]+)", out)]
    long_ = sum(p > 0.5 for p in pauses)
    return f"{len(pauses)} Pausen, zusammen {sum(pauses):.1f} s, davon {long_} über 0,5 s"


def words(text: str) -> list[str]:
    return re.findall(r"[a-zäöüß0-9]+", text.lower())


def check(text: str, path: str) -> int:
    import wave

    import numpy as np
    from faster_whisper import WhisperModel

    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "a.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ar", "16000",
                        "-ac", "1", wav], check=True)
        w = wave.open(wav)
        audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, language="de", beam_size=5)
    heard = words(" ".join(s.text for s in segs))
    said = words(text)
    problems = []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, said, heard, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        want, got = " ".join(said[a1:a2]), " ".join(heard[b1:b2])
        if any(c.isdigit() for c in want + got):  # Whisper writes numbers as digits
            continue
        problems.append(f"  Text: {want or '—'}  →  gehört: {got or '—'}")
    print("Pausen:", pause_stats(path))
    if problems:
        print(f"{len(problems)} Abweichung(en) — prüfen, ob es Aussprache ist (dann PRONUNCIATION) "
              "oder nur Schreibweise:")
        print("\n".join(problems))
    else:
        print("Aussprache: keine Abweichungen.")
    return len(problems)


async def synth(text: str, out_path: str, voice: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.mp3")
        await edge_tts.Communicate(prepare(text), voice).save(raw)
        tighten_pauses(raw, out_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text_file")
    ap.add_argument("out_mp3")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--check", action="store_true", help="transcribe and report mispronunciations")
    args = ap.parse_args()
    with open(args.text_file, encoding="utf-8") as f:
        source = f.read()
    asyncio.run(synth(source, args.out_mp3, args.voice))
    if args.check:
        check(source, args.out_mp3)
