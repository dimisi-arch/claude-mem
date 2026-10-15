---
id: 21
title: "short-video-studio: no length budget before recording, edge-tts silence padding, and no period/consistency check for images"
status: open
type: open-source
skill: [short-video-studio]
proposes_skill: []
target_file: []
siblings_checked: "none — short-video-studio belongs to no family (no skill-families.md)"
area: "Step 1 (story), steps 4-5 (voice), steps 2-3 (image check)"
date: 2026-10-15
session_context: "Producing a 9:16 history-mystery short (episode 1 of a 5-part series) with SDXL-Turbo and Microsoft Conrad voice"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — ffmpeg silencedetect on edge-tts output: ~0.22 s lead and ~1.0 s trailing silence per line, ~1.0 s between sentences; trimming with silenceremove (both ends via areverse, internal pauses capped at 0.24 s) took 17 lines from 70.8 s to 45.9 s"
---

**Issue:** Three gaps showed up in one production. (1) The skill has no length budget: a 126-word script came out at 70.8 s with Conrad at -6 %, while the target was ~45-50 s; the script had to be cut and re-recorded after images were already rendering. (2) edge-tts pads every line with ~0.2 s lead and ~1 s trailing silence plus ~1 s between sentences; with 17 lines that is ~20 s of dead air the skill never mentions. (3) The image step has no check for period accuracy or object count: SDXL-Turbo drew WWI steel helmets on 1906 Prussian soldiers, doubled pocket watches (two stacked watches in 3 of 5 watch shots), and cannot draw a 13-hour dial at all.

**Suggested improvement:** Step 1: add a words-per-second budget (measured ~2.2 words/s for Conrad -6 % after trimming) and size the script before recording. Steps 4-5: trim lead/trail silence and cap internal pauses in `stimme.py` (silenceremove + areverse), then add pauses deliberately in the cut. Steps 2-3: add a look-check list per image — period details (helmets, uniforms, vehicles), object count ("one single …"), recurring character identical, face rule — and say that a story object the model cannot draw (custom dial, sign text) is drawn in code and composited, not re-rolled.

**Principle:** Measure the narration's real speaking rate and padding before committing to a script length, and check generated images against the sentence for period and count errors, not just mood.
