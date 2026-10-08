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
- Group reservations: **table time (2 hours) only when Stelios asks for it** —
  he deleted it twice (Wed + Fri), still to confirm as a rule; ask for a **phone number**; offer a menu and ask for the budget
  per person. Check the weekday of every date.
- Never invent availability, prices or policies; ask Stelios. Only drafts —
  nothing is sent. Gmail connector exists but has not been used yet.
- Customer offers/files stay out of the repo (scratchpad only).
- Venue: the **OG (Obergeschoss)** can be booked exclusively for parties of up
  to **100 people**. For large parties, wait for start time and duration before
  quoting a Mindestverzehr or price (user 2026-10-08).
- Pricing facts from the user (2026-10-08): groups à la carte → Mindestverzehr
  **35 € per person** (food + drinks); exclusive OG Friday evening 17–21 h for
  50–60 people → Mindestverzehr 6.000 €; signature is always the standard one
  ("Stelios Dimitriou – Team Omonia"), even if older sent mails differ.
- Company: **Omonia Gastro GmbH**, Passagehof 24, 76133 Karlsruhe,
  Tel. 0721 48699720, info@omonia-karlsruhe.de, www.omonia-karlsruhe.de
  (from public directory listings, 2026-10-08; user to confirm).
- Offer template ("Vorlage Gruppenangebot", built from the user's
  Angebot .docx): intro, header block (Datum, Beginn, Verweildauer,
  Ansprechpartner/Tel., Ort/Personen), standard meze menu, Sekt + first round
  of water included, dessert only as optional add-on sentence, Menüpreis
  62,90 / Sonderpreis ohne Dessert 58,90, conditions (5 days, 50 %,
  allergies "vorab", no deadline, valid 14 days from issue date), contact signature.
  **Always use the latest version for every new offer** (user decision
  2026-10-08): `.claude/context/omonia/Vorlage_Gruppenangebot_Omonia.docx`
  (no customer data; yellow-highlighted [placeholders]). When the template
  changes, replace that file and commit it.
- Christmas menu template ("Weihnachtsmenü", 2 pages):
  `.claude/context/omonia/Vorlage_Weihnachtsmenue_Omonia.docx` — same meze
  menu, **3. Gang Dessert included** (Galaktoboureko mit Vanilleeis /
  Schokoladenkuchen), **no Sekt, no water** (all drinks by consumption),
  Menüpreis 62,90 € / **Sonderpreis 57,90 €** per person.
- Reply mails: send follow-ups **as a reply to the earlier mail** (thread);
  for invoice payment ask "vor Ort oder Rechnung" and offer the
  Kostenübernahme; ask for exact head count 5 days before.
- Cost-coverage form ("Kostenübernahmebestätigung", 1 page, Omonia logo):
  `.claude/context/omonia/Vorlage_Kostenuebernahmebestaetigung_Omonia.docx`.
  Sections: Veranstaltung, Rechnungsempfänger, Umfang (ganze Rechnung / nur
  Speisen / Höchstbetrag; always "inklusive Trinkgeld in Höhe von ___ %" — percent only), Zahlung ([14 Tage] payment term still to confirm),
  return note, signature + company stamp. For bookings paid by invoice, ask
  for it in the reply mail and attach a pre-filled copy (pre-filled copies
  stay in the scratchpad: customer data).

### Open cases (as of 2026-10-08; no guest names/phones here — repo is PUBLIC)

Guest contact data is NOT stored in this repo. Ask Stelios for the original
mail when picking a case up again.

| Date | Group | Status / next step |
|---|---|---|
| Fri 16.10.2026 17–21 h | school, 50–60 p., OG | offer sent (OG exclusive, MV 6.000 € or menu without exclusivity); no answer → reminder drafted, deadline Mon 12.10.2026 |
| Wed 04.11.2026 19:30 | company INIT, 21 p., à la carte, invoice | confirmation + pre-filled Kostenübernahme drafted |
| Mon 09.11.2026 18:00 | company BBBank, 25 p., Weihnachtsfeier | offer (menu 62,90 / 58,90) + 2-line confirmation drafted |
| Thu 26.11.2026 17:30 | ~30 p., Weihnachtsfeier, à la carte | first mail said MV 45 € (wrong) → correction to **35 €** + reminder drafted, deadline Fri 16.10.2026. Same evening: 20 p. at 18:30 (hostel group, menu + budget asked) — check space |
| Fri 27.11.2026 19:00 | company, ~20 p. | reply drafted (company name, menu/à la carte, payment, head count 5 days before) |
| Fri 11.12.2026 | company (medical centre), 25–30 p. | 04.12 fully booked; Christmas-menu offer (Sonderpreis 57,90) drafted; ask start time + payment |
| Thu 17.12.2026 18:30 | company BBBank, 13 p., à la carte | confirmation + payment question + pre-filled Kostenübernahme drafted |
| Sat 19.12.2026 | engagement party ≤100 p., OG exclusive | waiting for start time + duration before quoting MV/price; same day 16:30 20 p. (12 adults, 8 children, one long table, 2 high chairs) |
| Sat 05.12.2026 | private party, area exclusive | offered: MV 8.000 € exclusive, or without exclusivity → menu; music loud until 23:30, party until midnight |
| Fri 23.10.2026 17:00 | 20 p., thesis defence | reply drafted (2 h, phone, menu/budget) |

Open questions for Stelios: payment term in the Kostenübernahme ([14 Tage]?),
usual tip %, Büffet possible for 100 p.?, table-time rule, all-weekday rule.

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
