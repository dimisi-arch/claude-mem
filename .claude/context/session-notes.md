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

### Pending connections (user still has to finish OAuth)

As of the last check both were created but **incomplete** (no token):

| App | Credential request | Connection id(s) |
|---|---|---|
| Notion | `8b8297af-9f0a-40d9-bd30-c7bc3583683e` | `11692405`, `11692087` |
| Gmail | `4c2687c4-d9e6-4ab4-8b79-4b5b300a1717` | `11692409` |

Check with `credential-requests_get` / `connections_list` (team 3074487). The
user opens `https://eu1.make.com/3074487/credentials-requests/inbox?requestId=<id>`
and must click through to "Allow" in the Notion/Google window; alternative:
Make → Connections → Create a connection.

### Webhook

- Hook `3861381` "Anfragen → Notion" (gateway-webhook, team 3074487). Get its
  URL with `hooks_get`. Learning mode was started; payload not confirmed yet.

### Planned automations (not built yet)

1. **Webhook → Notion**: generic webhook (above) creates an item in a Notion
   data source. Field mapping waits on the first real request.
2. **Daily Notion summary by Gmail**: new/changed Notion items once a day.
   Proposed: 08:00 Europe/Berlin, recipient = the user's own address (confirm).
3. **AI sorting**: new Notion items get a category/priority from Make's AI
   Provider.

Open questions for the user: which Notion database, confirm recipient and
time, which property the AI sets and its allowed values. Build all three
scenarios inactive; activate only after the user has tested them.

## OmniRoute (github.com/diegosouzapw/OmniRoute) — DROPPED 2026-10-09

User decided to drop OmniRoute (free `auto` tier refused by OpenCode). Do not
pursue it further unless the user brings it up again. History below.


User wants Claude Code to run through it. Only possible on the user's own
machine (`npm install -g omniroute`, dashboard `localhost:20128`, then
`omniroute launch` or `ANTHROPIC_BASE_URL=http://localhost:20128` without
`/v1` plus `ANTHROPIC_AUTH_TOKEN`). Never set this in a cloud session. Caveats
already explained: code goes to third-party providers, some providers have
risky terms, non-Claude models work worse with Claude Code, ~8 GB RAM.
Offered next: per-project activation or Docker setup.

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

## task-observer

Installed in `.claude/skills/task-observer/`, activated in `CLAUDE.md`. The
shortened activation was used (the verbatim upstream block was not inserted).

## ponytail (2026-10-08)

Skills from github.com/DietrichGebert/ponytail (MIT) copied into
`.claude/skills/ponytail*` (6 skills, hooks left out), because `/plugin` does
not work in cloud sessions. On branch `claude/ponytail-plugin-install-60yz0p`;
available in every session only once merged into the main branch. Coding only;
not for the restaurant e-mails.

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

## frontend-design (2026-10-09)

Anthropic's `frontend-design` plugin skill (Apache 2.0) copied into
`.claude/skills/frontend-design/`. In cloud sessions `claude plugin install`
works only for the running container; the official marketplace is named
`anthropic-plugin-directory` here, not `claude-plugins-official`.

## agent-skills by Addy Osmani (2026-10-09)

User chose a selection of 7 of the 25 skills from github.com/addyosmani/agent-skills
(MIT), copied into `.claude/skills/`: idea-refine, interview-me,
planning-and-task-breakdown, spec-driven-development,
debugging-and-error-recovery, security-and-hardening, documentation-and-adrs.
Left out on purpose: overlaps (code review, simplification, frontend) and
skills that fire on every change (TDD, git workflow, using-agent-skills at
session start). Some copied skills mention test-driven-development /
incremental-implementation / observability-and-instrumentation, which are not
installed. Hooks and scripts of that repo not copied.

## graphify (2026-10-09)

User chose the full setup. CLI `graphifyy` (PyPI, double y = official name;
github.com/Graphify-Labs/graphify, MIT/Apache 2.0) is installed at every cloud
session start by `.claude/hooks/install-graphify.sh` (SessionStart, remote
only, never fails the start). `graphify install --project` added the skill
(`.claude/skills/graphify/`), `.claude/CLAUDE.md`, a graphify section in
`CLAUDE.md` and two PreToolUse hooks; the hooks were wrapped so they do
nothing when the CLI is missing. Graph for `src/` built 2026-10-09 (6322 nodes,
215 communities, ~464k tokens for 5 docs + 6 images); `graphify-out/` is
gitignored, so it is lost with the container unless the user asks to commit it.

## OmniRoute test in the cloud (2026-10-09)

User asked to test `curl localhost:20128/v1/chat/completions` with model
`auto` and open a PR if it works. Result: OmniRoute 3.8.51 installs and starts
(needs Node >= 22.22.2; container has 22.22.0, worked with node@24 from npm),
bound to 127.0.0.1 because the default listens on 0.0.0.0 without an API key.
The request failed: the free `auto` provider opencode.ai is blocked by the
environment's network policy. No PR opened because the test did not pass.
Nothing was routed through it; Claude Code settings untouched.
User's own Windows PC (2026-10-09): OmniRoute 3.8.51 installed and running
(PowerShell 7.6.6 available; npm skipped install scripts but the server still
started). Test with `auto` reached OpenCode, which answered HTTP 403 "free tier
can only be used from within OpenCode" — the README's zero-credential claim no
longer holds. Test not passed, so no PR. Dashboard password was still the
default "CHANGEME"; user told to change it. User pasted an OmniRoute API key in
chat; told to rotate it; not stored anywhere.

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

Fixed channel voice (user approved 2026-10-09): Runway preset **Elias**, model
eleven_v3, languageCode de, stability 0.5; [whispers]/[shouts] tags for drama.
Runway free plan: voice library search and music are not available; sound effects
work (1 credit/s). ~35 credits left after Short 1. Short 1 "Ich heisse Niemand"
was cut in the container (PIL frames -> ffmpeg, silencedetect for subtitle timing)
and awaits approval; the video file lived only in the scratchpad.
Short 1 v2 (user asked: faster, other voices for characters): narrator Elias sped
up 15% with atempo, character voices Odysseus=Clint (whisper), Polyphem=Monster
(pitched down, cave echo), other Cyclopes=Ragnar+Grungle chorus. Speaker name shown
above character subtitles. ~40 Runway credits left.

**Channel format decided 2026-10-09: Shorts only**, 40-60 s, 9:16, no long videos.
Each story is uploaded part by part; every part ends with a hook to the next part
(never "the whole story comes soon"). Channel description updated to say so (live).
Odysseus is spoken normally, not whispered. Short 1 v3 (47.7 s) ends "TEIL 2 FOLGT";
next: part 2, the escape under the rams. ~35 Runway credits left.
