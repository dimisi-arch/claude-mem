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

## OmniRoute (github.com/diegosouzapw/OmniRoute)

User wants Claude Code to run through it. Only possible on the user's own
machine (`npm install -g omniroute`, dashboard `localhost:20128`, then
`omniroute launch` or `ANTHROPIC_BASE_URL=http://localhost:20128` without
`/v1` plus `ANTHROPIC_AUTH_TOKEN`). Never set this in a cloud session. Caveats
already explained: code goes to third-party providers, some providers have
risky terms, non-Claude models work worse with Claude Code, ~8 GB RAM.
Offered next: per-project activation or Docker setup.

## task-observer

Installed in `.claude/skills/task-observer/`, activated in `CLAUDE.md`. The
shortened activation was used (the verbatim upstream block was not inserted).
