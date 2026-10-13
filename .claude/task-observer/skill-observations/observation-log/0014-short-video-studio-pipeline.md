---
id: 14
title: "Faceless short-video production is a repeatable studio pipeline (image, voice, subtitles, render) worth its own skill"
status: open
type: open-source
skill: []
proposes_skill: [short-video-studio]
target_file: []
siblings_checked: "none — no skill-families.md in this install; remotion-best-practices renders code-built animations and historical-images finds public-domain stills, neither covers AI frames + TTS + burned subtitles + Ken Burns (their descriptions)"
area: "Producing vertical story videos end to end in a cloud session"
date: 2026-10-13
session_context: "User wants a faceless TikTok/Shorts/Reels story channel and asked whether Claude can act as a full studio (images, render, cut); a 13.5 s test scene was produced end to end"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — Runway generate_image nano-banana-2-lite 9:16 (worked, 768x1376, 4 credits of 8; free plan has no video models); Canva generate-image (worked, but the tool returns only a 112x199 preview, full size stays in Canva); uv tool run --from piper-tts piper -m de_DE-thorsten-high.onnx (worked offline after downloading the voice from huggingface; mispronounces some words: 'schlug' heard as 'Schluck'); edge-tts via vorlesen.py: 403 from speech.platform.bing.com in the cloud; faster-whisper transcribe(path) fails with 'open() got an unexpected keyword argument metadata_errors' (PyAV mismatch) — decoding with ffmpeg to a 16 kHz numpy array works; ffmpeg zoompan + vignette + subtitles=ASS + amix (worked; the noise filter bloats size 14x, crf 23 without it gives 2.5 MB for 13.5 s)"
---

**Issue:** Asked whether Claude can be a whole studio, the agent assembled the pipeline by trial: which image tool returns a usable full-size file (Runway yes, Canva only a preview), which voice works in the cloud (edge-tts blocked, Piper offline works), how to get word-timed subtitles (faster-whisper breaks on file paths, works on ffmpeg-decoded audio; subtitles must use the script text, not the transcript, or TTS mispronunciations end up on screen), and the ffmpeg filter graph (zoom, vignette, ASS subtitles with a highlight colour, ticking sound bed, fades). Each of these took a failed call first.

**Suggested improvement:** New skill `short-video-studio`: input = a scene table (image prompt, narration per scene); steps = generate frames (Runway, fixed style prompt and character reference for consistency), narration (Piper offline or Runway speech, with a pronunciation respelling list), subtitles from the script aligned to measured speech, render per scene with ffmpeg and concatenate, then a QA frame grab. Ship the scripts (subs alignment, render command) inside the skill, and list costs per step and the plan limits (Runway free: images only).

**Principle:** When a multi-tool production chain is assembled once by trial, freeze the working chain (tools, flags, workarounds, cost per step) into a skill with its scripts, so the next run starts from the known-good path instead of re-discovering the same failures.
