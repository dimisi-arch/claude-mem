---
name: "voice-summary"
description: "Internal skill for this repo. Turn the answer to the user into a German voice message (MP3) and check it by ear-proxy before sending: write flowing spoken German, render with .claude/scripts/vorlesen.py, let --check transcribe it with Whisper, fix every misheard word in the script's PRONUNCIATION list and rerun until clean, then send the file. Use for the standing 'voice message with every answer' rule, or when the user asks for a spoken summary, Sprachnachricht or Vorlesen."
requires:
  - binary: ffmpeg
  - binary: uv
---

# Voice summary (internal)

The user listens to answers as voice messages, often while driving. They
judge them by ear, so every message is measured before it is sent: a
guessed fix ("try another voice", "slower") costs the user another round of
listening and complaining; a measured one does not.

The tool is `.claude/scripts/vorlesen.py` (free Microsoft voice via
edge-tts, needs internet and ffmpeg). It already trims long pauses and, with
`--check`, transcribes the result and lists every word that came out
differently from the text.

## 1 — Write for the ear

- Flowing spoken German in longer connected sentences, wir/du form as in the chat.
- No lists, links, brackets, abbreviations, file paths or digits: write
  numbers as words ("zwölf Beobachtungen", "Montag um Viertel vor sieben").
- English technical terms and skill names stay English (Main, Branch,
  Merge, Pull Request) — the script respells them so they sound English.
- After an English name, the voice may drift into English for the next
  German word ("Agent Reach sucht" → "sucked"): put a comma after the name
  or rephrase ("Mit Agent Reach suche ich …").
- Say what the user must do or decide; leave out what only matters on screen.

Save the text to a file in the scratchpad.

## 2 — Render and check

```bash
uv run --with edge-tts --with faster-whisper python .claude/scripts/vorlesen.py TEXT.txt OUT.mp3 --check
```

The check prints the pause statistics and each deviation as
`Text: … → gehört: …`.

## 3 — Fix every deviation, then rerun

For each line decide:

- **Pronunciation** (the voice said it wrong — almost always an English
  name): add a respelling to `PRONUNCIATION` in the script, longer names
  before shorter ones, with a comment naming what Whisper heard. Unsure
  which respelling works? Render one-sentence test clips of two or three
  variants with `--check` and keep the one Whisper hears correctly.
- **Spelling only** (Whisper wrote a correctly spoken word differently,
  e.g. compound words, numbers): leave it.

Rerun step 2 until no pronunciation deviation is left. Limits: Whisper
also mishears correct speech, and intonation cannot be measured this way;
a paid voice (ElevenLabs, Runway credits) is the real upgrade if the user
wants one.

## 4 — Send

Send the MP3 with `SendUserFile` together with the written answer. When
`PRONUNCIATION` changed, commit the script on the session's branch so the
next session hears the fix too.

## Pre-flight before sending

- [ ] Text has no digits, lists, links or paths
- [ ] `--check` ran on this exact file and shows no pronunciation deviation
- [ ] New respellings are in `PRONUNCIATION` with a comment
- [ ] MP3 sent with the written answer
