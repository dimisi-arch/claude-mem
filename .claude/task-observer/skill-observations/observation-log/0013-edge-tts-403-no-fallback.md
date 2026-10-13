---
id: 13
title: "Standing voice-message rule has no fallback when the Edge TTS endpoint answers 403 in the cloud"
status: open
type: internal
skill: []
proposes_skill: []
target_file: [".claude/scripts/vorlesen.py", ".claude/context/session-notes.md"]
siblings_checked: "none — the rule lives in session notes and a repo script, not in a skill"
area: "Voice message with every answer"
date: 2026-10-13
session_context: "Short content questions (viral shorts research); voice message attempted per standing rule"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run: uv run --with edge-tts --with faster-whisper python .claude/scripts/vorlesen.py in.txt out.mp3 --check -> aiohttp WSServerHandshakeError 403 from speech.platform.bing.com"
---

**Issue:** The session notes require a voice message with every answer via vorlesen.py (edge-tts). In this cloud session the Bing speech websocket answered 403, so the rule could not be met; the script has no fallback engine and the notes say nothing about what to do when it fails.

**Suggested improvement:** Give vorlesen.py a fallback TTS backend that works offline or through the proxy (e.g. a local model such as piper with a German voice), or add one line to the session notes: when TTS fails, say so once per session and continue in text.

**Principle:** A standing per-answer rule that depends on an external service needs a defined fallback, or every answer either fails the rule silently or burns time on retries.
