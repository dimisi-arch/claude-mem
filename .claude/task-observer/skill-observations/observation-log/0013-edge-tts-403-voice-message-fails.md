---
id: 13
title: "Voice message script fails in the cloud: Microsoft edge-tts answers 403, no fallback voice"
status: open
type: internal
skill: []
proposes_skill: [voice-summary]
target_file: [".claude/scripts/vorlesen.py"]
siblings_checked: "none — no skill covers spoken summaries yet; the script is the target, same as observation 10"
area: "Voice message sent with every answer (vorlesen.py, edge-tts backend)"
date: 2026-10-13
session_context: "Summarising an Instagram reel in a cloud session; the standing voice message could not be produced"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — uv run --with edge-tts --with faster-whisper python .claude/scripts/vorlesen.py in.txt out.mp3 --check: WSServerHandshakeError 403 from speech.platform.bing.com (edge-tts 7.2.8), twice; agent proxy status enabled and covers every host"
---

**Issue:** The standing rule says every answer comes with a German voice
message made by `.claude/scripts/vorlesen.py`. In this cloud session the
script crashed twice with a 403 from Microsoft's Edge read-aloud endpoint
(edge-tts 7.2.8, `--refresh-package edge-tts` gave the same version). The
script has no second voice backend, so the user got a text answer only. Root
cause not established: Microsoft token change, the cloud egress IP being
blocked, or clock-based `Sec-MS-GEC` mismatch are all possible.

**Suggested improvement:** Give `vorlesen.py` a fallback: on a 403 or
handshake error, print one clear German line ("Sprachdienst nicht erreichbar")
and exit non-zero quickly instead of a long traceback; consider a second
free TTS backend (e.g. a local Piper German voice) so the voice message
survives a blocked online service. Check from the PC whether edge-tts works
there — if yes, the block is cloud-specific.

**Principle:** A standing per-answer deliverable that depends on one free
online service needs a stated fallback and a short, readable failure
message; otherwise each outage costs a debugging detour mid-answer.
