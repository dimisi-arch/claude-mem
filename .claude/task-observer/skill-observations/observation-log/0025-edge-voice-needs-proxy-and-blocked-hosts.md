---
id: 25
title: "short-video-studio in a limited-network cloud session: model hosts blocked, Microsoft voice skipped because edge-tts ignores the HTTPS proxy, stalled model download"
status: open
type: internal
skill: [short-video-studio, voice-summary]
proposes_skill: []
target_file: [".claude/skills/short-video-studio/scripts/stimme.py", ".claude/scripts/vorlesen.py"]
siblings_checked: "none — no skill-families.md; voice-summary added because vorlesen.py uses the same edge-tts call (assumed, file not read this session)"
area: "Step 2 (images: network prerequisites) and Step 4 (voice engine order, edge function)"
date: 2026-11-09
session_context: "Producing an Odysseus/Sirens short in a cloud session whose environment had limited network access"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — curl to download.pytorch.org, huggingface.co, speech.platform.bing.com: proxy 403 until the hosts were allowed (also needed: download-r2.pytorch.org, us.aws.cdn.hf.co); run — stimme.py auto: edge failed with ClientConnectorDNSError and fell back to piper; run — edge-tts --proxy $HTTPS_PROXY: MP3 written; run — stimme.py copy with proxy=os.environ.get('HTTPS_PROXY') in edge_tts.Communicate: 8 lines 'edge'"
---

**Issue:** Three things cost about 25 minutes. (1) The environment's limited network blocked every host the image step needs; the skill lists none of them. (2) `stimme.py` skipped the Microsoft voice with a DNS error and silently used Piper, which mispronounced "Odysseus": edge-tts (aiohttp) does not read HTTPS_PROXY, it must be passed as `proxy=`. The skill blames "403 from some cloud IPs". (3) The SDXL download stalled at 3.4 of 5.1 GB for five minutes with no error; a restart began from zero.

**Suggested improvement:** In `stimme.py` (and, if it has the same call, `vorlesen.py`) pass `proxy=os.environ.get("HTTPS_PROXY")` to `edge_tts.Communicate`. Add a "Network prerequisites" line to SKILL.md step 2 with the host list (huggingface.co, us.aws.cdn.hf.co, download.pytorch.org, download-r2.pytorch.org, speech.platform.bing.com, api.fish.audio) and a one-line curl pre-check. Start `bilder.py` with `HF_HUB_DOWNLOAD_TIMEOUT=30` and note that a download whose .incomplete file stops growing is restarted.

**Principle:** A skill that fetches models or calls services names its hosts and checks them before the first long step; a fallback chain reports why a better engine was skipped, and a library that ignores proxy variables gets the proxy passed explicitly.
