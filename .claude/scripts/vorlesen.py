"""Turn a German text file into an MP3 voice message (the user's chat summaries).

Run: uv run --with edge-tts python .claude/scripts/vorlesen.py TEXT.txt OUT.mp3 [VOICE]
Default voice: de-DE-FlorianMultilingualNeural (male; reads English names like
"Agent Reach" correctly). Uses Microsoft's free online voices, so it needs internet.
"""

import asyncio
import os
import sys

import certifi

# Cloud containers route HTTPS through a proxy with its own CA; edge-tts only trusts certifi.
if os.environ.get("SSL_CERT_FILE"):
    certifi.where = lambda: os.environ["SSL_CERT_FILE"]

import edge_tts  # noqa: E402 (must follow the certifi patch)


async def main(text_path: str, out_path: str, voice: str) -> None:
    with open(text_path, encoding="utf-8") as f:
        text = f.read()
    await edge_tts.Communicate(text, voice, rate="-5%").save(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "de-DE-FlorianMultilingualNeural"))
