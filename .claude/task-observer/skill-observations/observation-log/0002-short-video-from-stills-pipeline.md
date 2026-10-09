---
id: 2
title: "Recurring workflow: cut a narrated vertical Short from still images, voiceover and subtitles in the container"
status: open
type: open-source
skill: []
proposes_skill: [short-video-from-stills]
target_file: []
siblings_checked: "none: no installed skill covers video assembly; frontend-design, canvas-design and the Runway connector were checked and none renders video"
area: "new skill: video assembly from stills + TTS"
date: 2026-10-09
session_context: "Producing the first YouTube Short for a history channel: TTS voice from an image/audio generator, existing scene stills, automatic cut in the cloud container"
parked_until:
resolved:
resolution:
reference:
commands_verified: "none"
---

**Issue:** The channel plan calls for 3 to 4 Shorts per episode, each built the same way: pick stills, generate a voiceover, align subtitles to the speech, add slow zoom/pan (Ken Burns), crossfades, a title card, an end card with the channel logo, a quiet ambience bed, loudness normalisation, then mux to 1080x1920 H.264. This session built it from scratch (PIL frame renderer piped into ffmpeg, ffmpeg silencedetect for subtitle timing, amix + loudnorm for audio). The first render had three defects that only a frame check caught: the title word overflowed the frame width, a trailing ellipsis wrapped onto its own line (Python `str.split()` also splits on a no-break space), and end-card subtitles overlapped the logo.

**Suggested improvement:** A skill `short-video-from-stills` with: a shot list format (start, end, image, start/end focus point and zoom, optional shake); subtitle timing from silencedetect segments mapped to script sentences, long sentences split by character share; text auto-fit to the frame width; a subtitle safe zone for vertical-video UIs (centre around y=1260 of 1920, max width ~860); a fixed check step that extracts frames at each segment and at every title or end card before delivery; audio recipe (voice + looped ambience at about -16 dB, fades, loudnorm I=-14 TP=-1.5).

**Principle:** When a deliverable is rendered rather than written, the verification step is a look at sampled output frames at every layout change, not a check that the command exited 0. Layout defects (overflow, orphaned words, overlaps) are invisible to the renderer and obvious in one frame.
