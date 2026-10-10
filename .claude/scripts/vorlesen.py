"""Turn a German text file into an MP3 voice message (the user's chat summaries).

Run: uv run --with edge-tts python .claude/scripts/vorlesen.py TEXT.txt OUT.mp3 [VOICE]
Default voice: de-DE-FlorianMultilingualNeural (male; the user likes its pitch). Uses
Microsoft's free online voices, so it needs internet.

Write the text as flowing spoken German: longer connected sentences, no lists, links,
brackets or abbreviations — short choppy sentences are what make it sound "abgehackt".
"""

import asyncio
import os
import re
import sys

import certifi

# Cloud containers route HTTPS through a proxy with its own CA; edge-tts only trusts certifi.
if os.environ.get("SSL_CERT_FILE"):
    certifi.where = lambda: os.environ["SSL_CERT_FILE"]

import edge_tts  # noqa: E402 (must follow the certifi patch)

# English names the German voice gets wrong, respelled so it says them right. Checked
# 2026-10-10 by transcribing the audio with Whisper: "Claude" came out as "Cloud", "GitHub"
# as "Getub". Agent Reach, Headroom, Anthropic, Notion and Setup were already correct.
PRONUNCIATION = {
    "Claude": "Clawd",
    "GitHub": "Git Hub",
}


def prepare(text: str) -> str:
    for word, spoken in PRONUNCIATION.items():
        text = re.sub(rf"\b{re.escape(word)}\b", spoken, text)
    # Hard line breaks inside a paragraph make the voice pause mid-sentence.
    paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text)]
    return "\n\n".join(p for p in paragraphs if p)


async def main(text_path: str, out_path: str, voice: str) -> None:
    with open(text_path, encoding="utf-8") as f:
        text = prepare(f.read())
    await edge_tts.Communicate(text, voice).save(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "de-DE-FlorianMultilingualNeural"))
