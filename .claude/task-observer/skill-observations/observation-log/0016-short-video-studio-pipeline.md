---
id: 16
title: "Faceless short-video production is a repeatable studio pipeline (image, voice, subtitles, render) worth its own skill"
status: actioned
type: open-source
skill: []
proposes_skill: [short-video-studio]
target_file: []
siblings_checked: "none — no skill-families.md in this install; remotion-best-practices renders code-built animations and historical-images finds public-domain stills, neither covers AI frames + TTS + burned subtitles + Ken Burns (their descriptions)"
area: "Producing vertical story videos end to end in a cloud session"
date: 2026-10-13
session_context: "User wants a faceless TikTok/Shorts/Reels story channel and asked whether Claude can act as a full studio (images, render, cut); a 13.5 s test scene was produced end to end; 2026-10-14: full 58 s episode Die Kamera lügt (dark comic, deeper voice)"
parked_until:
resolved: 2026-10-15
resolution: "New skill .claude/skills/short-video-studio built on the user's request (2026-10-15): projekt.json-driven scripts (bilder, kontakt, stimme Fish>Microsoft>Piper, pruefen, schnitt) from the reference scripts, all traps of the three instances built in (style first + 77-token warning, -nostdin, pid file not pgrep, bitrate cap, subtitles from script, OOM-safe model choice); tested end to end in the cloud 2026-10-15 (3 scenes, 21 s, 5.5 MB)"
reference: ".claude/task-observer/skill-observations/references/short-video-studio/ (bilder.py, schnitt.py, kontakt.py, sprechen.sh, aussprache.sed, pruefen.py, szenen.json, auswahl.json)"
commands_verified: "run — Runway generate_image nano-banana-2-lite 9:16 (worked, 768x1376, 4 credits of 8; free plan has no video models); Canva generate-image (worked, but the tool returns only a 112x199 preview, full size stays in Canva); uv tool run --from piper-tts piper -m de_DE-thorsten-high.onnx (worked offline after downloading the voice from huggingface; mispronounces some words: 'schlug' heard as 'Schluck'); edge-tts via vorlesen.py: 403 from speech.platform.bing.com in the cloud; faster-whisper transcribe(path) fails with 'open() got an unexpected keyword argument metadata_errors' (PyAV mismatch) — decoding with ffmpeg to a 16 kHz numpy array works; ffmpeg zoompan + vignette + subtitles=ASS + amix (worked; the noise filter bloats size 14x, crf 23 without it gives 2.5 MB for 13.5 s); local SDXL-Turbo (diffusers, torch CPU, bfloat16 on a 4-core AMX Xeon, 576x1024, 4 steps) ~25 s per image, 45 images for one episode at zero cost (worked); full 77 s episode render from 13 stills + 13 Piper lines ~90 s (worked); whisper check of each TTS line found 3 mispronounced words (nassem, Zeitungsjunge, Zuchthaus), fixed by respelling or rewording; running whisper in parallel with image generation tripled image time (CPU contention); libass stacks overlapping subtitle events — end times must be clipped to the next start"
---

**Issue:** Asked whether Claude can be a whole studio, the agent assembled the pipeline by trial: which image tool returns a usable full-size file (Runway yes, Canva only a preview), which voice works in the cloud (edge-tts blocked, Piper offline works), how to get word-timed subtitles (faster-whisper breaks on file paths, works on ffmpeg-decoded audio; subtitles must use the script text, not the transcript, or TTS mispronunciations end up on screen), and the ffmpeg filter graph (zoom, vignette, ASS subtitles with a highlight colour, ticking sound bed, fades). Each of these took a failed call first.

**Second instance (same session):** user asked for the images to be made 'with your own program' — local SDXL-Turbo on the CPU replaced paid image services; the whole episode (story, 13 images in 3 variants each, picked from contact sheets, voice, subtitles, sound, render) was produced in one session with scripts bilder.py, schnitt.py, kontakt.py and ton/sprechen.sh.

**Suggested improvement:** New skill `short-video-studio`: input = a scene table (image prompt, narration per scene); steps = generate frames (Runway, fixed style prompt and character reference for consistency), narration (Piper offline or Runway speech, with a pronunciation respelling list), subtitles from the script aligned to measured speech, render per scene with ffmpeg and concatenate, then a QA frame grab. Ship the scripts (subs alignment, render command) inside the skill, and list costs per step and the plan limits (Runway free: images only).

**Principle:** When a multi-tool production chain is assembled once by trial, freeze the working chain (tools, flags, workarounds, cost per step) into a skill with its scripts, so the next run starts from the known-good path instead of re-discovering the same failures.

**Second instance (2026-10-14, episode "Die Kamera lügt", 58 s, dark comic style):** four more pipeline traps a skill would have prevented: (1) SDXL's CLIP encoder truncates prompts at 77 tokens, so a style string appended AFTER the scene prompt was silently cut; the style must come first and stay short. (2) `ffmpeg` inside a `while read` loop eats the loop's stdin and drops lines; needs `-nostdin`. (3) `pkill -f <script>` from the same shell killed the shell itself (its own command line matched). (4) "deeper, more suspenseful voice" was met with ffmpeg `rubberband=pitch=0.86:formant=preserved` + slower Piper `--length-scale`; a strong echo hurt Whisper intelligibility, so the check (median F0 via librosa pyin before/after + Whisper transcript) belongs in the pipeline as the verification step. Image models cannot draw "shadows of feet under the door": compositing the light gap with PIL on an existing frame worked.
