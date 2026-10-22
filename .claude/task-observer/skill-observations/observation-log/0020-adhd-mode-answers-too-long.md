---
id: 20
title: "ADHD mode active, but long multi-section answers still sent; user reminded 'ich habe adhs'"
status: actioned
type: internal
skill: [i-have-adhd]
proposes_skill: []
target_file: [".claude/hooks/session-start.sh"]
siblings_checked: "none — i-have-adhd belongs to no family (no skill-families.md)"
area: "Rules 1, 3, 9 (next action first, one next action, max 5 items) in long work sessions"
date: 2026-10-15
session_context: "After a long session (merge PRs, hooks, voice fallback, short-video-studio skill) the final report had 5 sections, ~20 bullets and the action not in line 1; the user replied only 'ich habe adhs'"
parked_until:
resolved: 2026-10-23
resolution: "Fixed final-answer shape added to the ADHD block injected by .claude/hooks/session-start.sh (line 1 action, max 3 done, max 2 open); i-have-adhd itself untouched (third-party). Structural Stop-hook only on a second violation"
reference:
commands_verified: none
---

**Issue:** The ruleset was injected by the start hook and loaded, yet the end-of-work report after a big multi-task turn ignored it: several headed sections, more than five items per group, a recap of everything done. The user's only reply was "ich habe adhs". Protection in play: written down and loaded into context, no checkpoint. Long tool-heavy turns end with a report written in the default "full summary" habit.

**Suggested improvement:** Add a final-answer shape to the hook's ADHD block: line 1 = the one thing to do now; then at most 3 lines "erledigt"; then at most 2 open points; details only in the PR. If it happens again, make it structural (e.g. a Stop hook that flags a final answer over ~15 lines while ADHD mode is on).

**Principle:** A style rule loaded at session start fades over a long tool-heavy turn; the end-of-turn report needs its own fixed shape, because that is where the default summary habit returns.
