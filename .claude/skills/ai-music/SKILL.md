---
name: ai-music
description: "Internal skill for this repo. Generate royalty-free background music for Shorts and videos with ACE-Step 1.5 through the free acemusic.ai cloud API (instrumental by default, 15-240 s, several variations). Use when a video needs music, a sound bed, a jingle or a mood track, e.g. for Age of Geschichte episodes or short-video-studio projects. Not for narration or voices (short-video-studio, vorlesen.py) or for sound effects."
requires:
  - env: ACEMUSIC_API_KEY
---

# AI music (internal)

One script, standard library only: `scripts/musik.py`. The user is not a developer:
report in one German line and send the MP3 instead of describing it.

## Setup (once)

- Free key: https://acemusic.ai/api-key (account with the user's own login).
- **Cloud:** the user adds `ACEMUSIC_API_KEY` in the environment settings (cloud
  environment menu in the session title bar → Edit → environment variables). A new
  session picks it up. Never ask for the key in chat.
- **PC:** one line in `~/.config/acemusic/key`.
- Without the key the script stops at once with that instruction (exit 1).

## Use

```bash
python3 .claude/skills/ai-music/scripts/musik.py "<style in English>" OUT.mp3 --sekunden 60 --varianten 3
```

- The answer takes 1-3 minutes (the API is slow; even a 401 took ~50 s from the cloud).
  Run it in the background for more than one variation.
- Prompt in English, short and concrete: genre, instruments, mood, tempo. Sparse prompts
  sound less samey. For Age of Geschichte: `"ancient greek lyre and frame drum, mysterious,
  slow build, cinematic, no vocals"`; tension: `"dark low strings, heartbeat drum, suspense"`.
- Always generate 2-3 variations, send them, let the user pick.
- Make the track a few seconds longer than the video; the cut fades it out.
- In short-video-studio set `"ton": {"musik": "musik.mp3"}` in `projekt.json`; keep the
  music well under the voice (the cut already mixes it low).

## Rights

ACE-Step 1.5 is MIT-licensed and its model card allows commercial use of generated music.
acemusic.ai publishes no separate terms for the free key (checked 2026-10-15): before
monetising, check its site for current terms. No Content ID claims are expected, but
keep the prompt and the file in the episode folder as proof of origin.
