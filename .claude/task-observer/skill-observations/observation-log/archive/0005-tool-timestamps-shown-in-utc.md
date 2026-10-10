---
id: 5
title: "Tool timestamps reported to the user in UTC instead of their local time"
status: actioned
type: open-source
skill: []
proposes_skill: []
target_file: [".claude/context/session-notes.md"]
siblings_checked: "none — the fix is a user-profile line, not a skill rule"
area: "Reporting times from tool results (Make, Tally, Notion)"
date: 2026-10-09
session_context: "Tally -> Make -> Notion webhook test; the agent quoted 23:49 / 23:52 from tool results, the user replied 'Wir haben 01:54'"
parked_until:
resolved: 2026-10-09
resolution: "User section of session-notes.md now states the time zone (Europe/Berlin) and that tool timestamps are UTC"
reference:
commands_verified: "none"
---

**Issue:** Make, Tally and Notion return timestamps in UTC (`...Z`). The agent
repeated them as plain clock times ("um 23:49"), two hours off for a user in
Germany (CEST, UTC+2). The user had to correct it.

**Suggested improvement:** Keep the user's time zone in the carried-over user
profile, and convert every `Z` timestamp before quoting it.

**Principle:** A timestamp ending in Z is UTC; convert it to the user's time
zone before showing it, and keep that zone where every session reads it.
