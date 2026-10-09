# Session notes — carried-over state

Stand: 2026-10-08. Written at the end of a session so the next one can pick up.
Verify anything time-sensitive (connection status, webhook) with the Make tools
before acting on it.

## User

- Answer in **German**.
- Not a developer: explain steps plainly, give copy-paste commands, ask before
  anything hard to undo.

## Restaurant e-mail assistant (main use since 2026-10-08)

- User = **Stelios Dimitriou**, works at **Restaurant Omonia** (Greek meze &
  kitchen bar). Claude drafts replies to guest e-mails and reservations and
  edits offers (Angebote, .docx with Omonia logo → also deliver as PDF with
  a preview image).
- **Proactively show improvement suggestions** for every text drafted, unasked
  (user request 2026-10-08).
- Style: German, "Sehr geehrte/r …", wir-Form, closing
  "Mit freundlichen Grüßen / Stelios Dimitriou / Team Omonia".
- Group reservations: mention **2 hours** table time and ask whether that is
  enough; ask for a **phone number**; offer a menu and ask for the budget
  per person. Check the weekday of every date.
- Never invent availability, prices or policies; ask Stelios. Only drafts —
  nothing is sent. Gmail connector exists but has not been used yet.
- Customer offers/files stay out of the repo (scratchpad only).
- Company: **Omonia Gastro GmbH**, Passagehof 24, 76133 Karlsruhe,
  Tel. 0721 48699720, info@omonia-karlsruhe.de, www.omonia-karlsruhe.de
  (from public directory listings, 2026-10-08; user to confirm).
- Offer template ("Vorlage Gruppenangebot", built from the user's
  Angebot .docx): intro, header block (Datum, Beginn, Verweildauer,
  Ansprechpartner/Tel., Ort/Personen), standard meze menu, Sekt + first round
  of water included, dessert only as optional add-on sentence, Menüpreis
  62,90 / Sonderpreis ohne Dessert 58,90, conditions (5 days, 50 %,
  allergies [3 days?], valid until), contact signature. Lived only in the
  scratchpad — ask the user for the file if needed again.

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

## YouTube-Kanal "Age of Geschichte" (since 2026-10-06)

All state lives in Notion, not the repo: page "Geschichtskanal: Kanal-Zentrale"
(https://app.notion.com/p/3f19d8bfe487816cb6f3ef3b6a91814e) with the
Redaktionsplan database (data source `collection://b43fdbca-d689-49a1-9c6f-c5416289d347`)
and the work page "Folge 1: Odysseus und der Zyklop"
(https://app.notion.com/p/3f09d8bfe487817597f0fa871ff23d78). Read those first.
Channel @AgeofGeschichte, ID UC4bC24FPFm1wovpWGNfhL1A. Make YouTube connection
to use: "YouTube dimisi300". vidIQ is connected as dimisi@gmx.de but lists no
channel. 2026-10-09: 0 videos. Channel description (all eras, "Age of ..." style,
German only, no English) set via Make scenario 7864799 "Kanalbeschreibung setzen
(Age of Geschichte)" (inactive; edit its mapper and run it to change the text) and
verified live; banner kept. Profile picture cannot be set by API: user uploads it
in YouTube Studio (Runway task 0b5af735, "Buch der Geschichte").

## Installed skills and tools (details: session-notes-archive.md)

- Repo skills in `.claude/skills/` (gitignored dir, new files need `git add -f`):
  task-observer, ponytail* (MIT, hooks left out: start with `/ponytail`),
  frontend-design, 7 agent-skills by Addy Osmani, graphify, Make skills,
  own `install-third-party-skill` (use it for every new third-party skill).
- `remotion-best-practices`: fetched at start by `.claude/hooks/install-remotion-skill.sh`
  (Remotion License, kept out of the repo). Rendering works with
  `--browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.
- graphify: `.claude/hooks/install-graphify.sh` installs the CLI and builds
  `graphify-out/` in the background (~2 min, no API cost).
- Start hooks only fire when this repo is the session's project; manual
  fallback in `CLAUDE.md`.
- OmniRoute: dropped 2026-10-09, do not pursue unless the user asks.

