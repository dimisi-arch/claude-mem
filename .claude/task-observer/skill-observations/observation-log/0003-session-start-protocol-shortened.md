---
id: 3
title: "Session Start Protocol run as a hand-made ls instead of the shipped commands"
status: open
type: open-source
skill: [task-observer]
proposes_skill: []
target_file: []
siblings_checked: "none — task-observer belongs to no family in this install (no skill-families.md)"
area: "Session Start Protocol, steps 1-2"
date: 2026-10-09
session_context: "Cloud session 'Funktioniert remotion?': the agent replaced steps 1-2 with one improvised ls/awk call; the gap surfaced only when the user asked for the review later in the session"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — workspace creation command at review time printed created=none"
---

**Issue:** At session start the agent invoked the skill and then ran one
improvised `ls` + frontmatter `awk` over the log instead of the workspace
creation command (step 1) and the guarded scan snippet (step 2). Nothing was
missing this time (created=none), but the checkpoint trace for the session was
not written and the starter-set reconciliation offer (marker absent, starter
set version 3) was never made. The trigger was a short user question that did
not look like a "task", plus a very long SKILL.md whose snippets have to be
hand-substituted with the workspace path before they can run.

**Suggested improvement:** Ship a `scripts/session-start.sh <workspace>` that
runs steps 1-3 (creation, scan with guards, review-date check, starter marker
check) and prints the one-line summary, so the protocol is one call like
`new-observation.sh` already is for writes. SKILL.md step 1 then names that
script as the only path, as it does for id derivation.

**Principle:** A procedure that must run at the start of every session should
be one executable call, not a set of snippets the agent has to adapt; an agent
under time pressure replaces adaptable snippets with a cheaper improvisation.

**Review 2026-10-09:** task-observer is foreign-maintained (metadata.source
github.com/rebelytics/one-skill-to-rule-them-all), so no local edit. User
chose "keep as a note" — parked, not sent upstream.

**Second instance, 2026-10-10 (scheduled weekly review, test firing):** the run
again replaced the step-2 scan snippet with a hand-made `ls` + `awk` over the
frontmatter; no checkpoint line was written. Second violation of the same
rule → the fix must be structural: the staged 3.6.0 `scripts/session-start-scan.sh`
is that barrier once installed, and the routine prompt / session-start hook
should then name that script as the one call.

**2026-10-10 (installed):** park condition met — task-observer 3.6.0 is
installed. Step 2 is now one command (`scripts/session-start-scan.sh`) and
is named as that one call in `.claude/hooks/session-start.sh` and CLAUDE.md.
Still open: steps 1 (workspace creation) and 3 (review trigger) have no
one-call command; that part is upstream's (rebelytics).
