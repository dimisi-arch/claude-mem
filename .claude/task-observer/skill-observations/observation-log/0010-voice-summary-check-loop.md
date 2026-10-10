---
id: 10
title: "Spoken summaries need a measure-and-fix loop (transcribe, respell, trim pauses), not a better-sounding voice choice"
status: open
type: internal
skill: []
proposes_skill: [voice-summary]
target_file: [".claude/scripts/vorlesen.py"]
siblings_checked: "none — no existing skill covers spoken summaries; no skill-families.md in this install"
area: "Voice messages sent to the user with every answer"
date: 2026-10-10
session_context: "User listens to every answer as a German voice message (driving, on the phone) and asked three times for more fluent speech and correct English pronunciation"
parked_until:
resolved:
resolution:
reference: ".claude/scripts/vorlesen.py (PRONUNCIATION list, MAX_PAUSE, --check)"
commands_verified: "run — uv run --with edge-tts --with faster-whisper python .claude/scripts/vorlesen.py TEXT OUT --check: reported 11 deviations on one message (Impeccable → 'impact käbel', Make → 'meg', Find → 'fine'); after respelling and pause trimming 0 pauses over 0.5 s (was 17) and silence 11.3 s (was 19.1 s of 100 s)"
---

**Issue:** The user's complaints ("abgehackt", English names wrong) were first answered by guessing: a different voice, a slower rate, "write longer sentences". None of that was verifiable, so each round ended with the user having to listen and complain again. What worked was measuring: (1) Whisper transcribes the audio and a word diff against the text shows exactly which words were misheard — i.e. mispronounced; (2) silencedetect shows the choppiness is pause time (19 % of the audio, 17 pauses over 0.5 s), which a frame-wise trim fixes. ffmpeg's `silenceremove` did not shorten the pauses at any threshold; a numpy RMS trim did. The user now wants every message checked before sending.

**Suggested improvement:** Turn the workflow into a small `voice-summary` skill (or a section in an existing one): write flowing spoken German without digits or lists → `vorlesen.py --check` → for each deviation decide pronunciation vs. spelling → add a respelling to PRONUNCIATION (test variants in one-sentence clips) → rerun until clean → send. Keep the list of tested respellings in the script, each with what Whisper heard. Note the limits: Whisper also mishears correct speech, and fluency beyond pauses (intonation) cannot be measured this way; a paid voice (ElevenLabs/Runway credits) is the real upgrade.

**Principle:** When a user judges output by ear or eye, build an automatic proxy measurement for their complaint (transcription diff, pause statistics) and iterate against it before handing over — otherwise every iteration costs a round-trip with the user.
