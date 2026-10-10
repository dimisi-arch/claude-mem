# Session notes — carried-over state

Stand: 2026-10-10.
Verify anything time-sensitive (connection status, webhook) with the Make tools
before acting on it.

## User

- Answer in **German** — every message, also the short status lines between tool
  calls, and PR descriptions on GitHub (user's reminder 2026-10-10).
- Time zone **Europe/Berlin**. Make/Tally/Notion timestamps are UTC (`…Z`):
  convert before quoting (CEST = UTC+2, CET = UTC+1).
- Not a developer: explain steps plainly, give copy-paste commands, ask before
  anything hard to undo.
- **Voice message with every answer** (standing): flowing spoken German, numbers as
  words, no links. Always run `uv run --with edge-tts --with faster-whisper python
  .claude/scripts/vorlesen.py in.txt out.mp3 --check`, fix every mispronounced word in
  its PRONUNCIATION list and rerun until clean, then SendUserFile. Voice pitch is right.

## Projects (private repos since 2026-10-10)

- Restaurant guest e-mails, offers, reservations: **`dimisi-arch/omonia-assistent`**
  (private). Its CLAUDE.md and notes hold the rules and state. Never copy guest or
  business details into this public repo.
- YouTube channel "Age of Geschichte": **`dimisi-arch/age-of-geschichte`** (private),
  with the style prompt and Notion links. Shared tools (historical-images, vorlesen.py)
  stay here.
- Start a session with the project repo plus claude-mem.

## Make (make.com)

- Access: Make MCP through the claude.ai **Make connector** (tools `mcp__Make__*`).
  The official `make` plugin is **not** installed in cloud sessions; its skills
  live in this repo instead (`.claude/skills/make-scenario-*`, command
  `/make-docs`). Load `make-scenario-building` before building a scenario.
- Account: zone `eu1.make.com`, organization `9206683`.
  - Team `3074487` "My Team" (default for new work)
  - Team `3074489` private space
- Existing connection: "Make's AI Provider (default)" (`11640039` in team 3074487).

### Connections (checked 2026-10-09)

- Gmail `11692409`: authorised, valid until 2027-04; used by the scenario
  "Redaktionsplan: tägliche Zusammenfassung per Gmail".
- Notion: use `11692396` "Notion Kanal-Zentrale" (used by the Redaktionsplan
  scenario). `11691665` is an unused duplicate. The old ids `11692405` and
  `11692087` no longer exist.
- YouTube: use "YouTube dimisi300" (3 scenarios); two other YouTube
  connections are unused duplicates.

### Scenarios

- **7871546 "Anfragen → Notion (Tally-Webhook)"** — **active since 2026-10-09**,
  tested end to end. Tally form "Kontaktformular" (id `81vZgo`,
  https://tally.so/r/81vZgo; fields Betreff, Name, E-Mail, Telefon, Nachricht)
  → hook `3861381` → Notion database "Anfragen" (data source
  `2fdf1501-26ae-4a9c-8da1-80e9f8c7fb7f`, shared with Make, connection 11692396).
  Fields are mapped by label from `data.fields`: renaming a Tally question
  breaks its column. Tally only sends new submissions from the live link (not
  the editor preview). Tally connector exists in claude.ai, but cannot set
  webhooks.
- **7853579** daily Redaktionsplan summary by Gmail (built, inactive).

### Planned automations

- **AI sorting**: new "Anfragen" items get a category/priority from Make's AI
  Provider. Open: which property and allowed values.

Build scenarios inactive; activate only after the user has tested them.

## Chat-Archiv in Notion (standing request)

User wants every chat saved to Notion, sorted by category. Database
"Chat-Archiv" (private), data source `collection://0f9aa644-8d33-447f-b637-7956de2e7e36`,
URL https://app.notion.com/p/225ef91bd7d44d73aa64bead77d66332.
Properties: Titel, Kategorie (Coding, Make & Automatisierung, Notion & Tools,
Lernen & Ideen, Entscheidungen, Sonstiges), Datum, Zusammenfassung,
Offene Punkte, Status (Offen/Erledigt), Sitzung (URL).

Rule for every session: before it ends (and after each larger topic), add one
page per topic with summary, decisions and open points. Summaries only, no
verbatim transcripts. Nothing runs by itself after a session closes; if the
user ends abruptly, the entry is missing. Created 2026-10-08 with three
entries from the first session.

## Code-Sammlung in Notion (standing request, 2026-10-08)

User wants every command / code snippet they paste into the chat saved for later
reuse when writing code. Private Notion page "Code-Sammlung"
(https://app.notion.com/p/3f39d8bfe48781a69c84fa1ec674daa5), not the repo —
the repo is public. Rule for every session: add each pasted snippet as a new
section at the top (title, date, what it is for, code block, status
✅ checked / ⚠️ unchecked / ❌ do not run, plus a safety note). Never store
passwords or API keys there; tell the user and leave them out. When the user
writes code, check the page for a fitting snippet first. Entries so far:
ponytail plugin commands, Voice Studio PowerShell installer (unchecked).

## Installed skills and tools (details: session-notes-archive.md)

- Repo skills in `.claude/skills/` (gitignored dir, new files need `git add -f`):
  task-observer, ponytail* (MIT, hooks left out: start with `/ponytail`),
  frontend-design, 7 agent-skills by Addy Osmani, graphify, Make skills,
  own `install-third-party-skill` (use it for every new third-party skill).
- `remotion-best-practices`: fetched at start (Remotion License). Render with
  `--browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.
- graphify, agent-reach and the free lists come from start hooks; they only fire
  when this repo is the session's project (manual fallback in `CLAUDE.md`).
- agent-reach (MIT, v1.5.0; details in its SOURCE.md): Exa search works in the
  cloud. Open: Reddit/Instagram only on the PC, with a secondary account.
- claude-automation-recommender (read-only), find-skills (search only), impeccable (web UI).
- Own skills (2026-10-10): `historical-images` (free museum images per episode) and
  `free-resources` (public-apis, free-for-dev, awesome-mcp-servers, fetched at start).

## Self-improvement loop (2026-10-10)

- Routine `trig_01S8wUrZaHJPHUUdTfQi5RbE` "Skill-Verbesserung (jeden 2. Tag)", 06:45
  Berlin (odd days), fires into session `session_01Lrn7FyucuYZy1VNQJZTC16` (has the repo; fresh
  routine sessions cannot push). Result: PR + push notification, never merges.
  "Run now" starts an empty session: test by messaging that session instead.
- `observer-nudge.sh` (UserPromptSubmit) reminds to log observations every 4th prompt.

## Local PC (workbench since 2026-10-10)

- Windows 11, repo at `C:\Users\Stilianos\claude-mem`; fork clone
  `C:\Users\Stilianos\playwright` (`upstream` = microsoft/playwright, built).
- Installed: Git, Node 24, uv, GitHub CLI, Chrome, Edge.
  No system Python: uv provides `python`/`python3` 3.13 and `graphify` in
  `C:\Users\Stilianos\.local\bin` (install with `uv tool install --python 3.13
  graphifyy`; newer Pythons need a C++ compiler). Put that folder first on
  PATH, else the Windows Store stub answers `python3`.
- Run repo scripts with Git Bash (check script and hooks work there). The
  Remotion/graphify hooks skip outside the cloud: skill fetched by hand.
- More PC details (Remotion browser path, PC-only skills): archive.
