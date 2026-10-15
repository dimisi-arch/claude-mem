---
id: 18
title: "Fetch-at-start hook pattern never installs a bumped REV: it exits as soon as the skill folder exists"
status: open
type: open-source
skill: [install-third-party-skill]
proposes_skill: []
target_file: []
siblings_checked: "none — install-third-party-skill belongs to no family (no skill-families.md)"
area: "Step 4b — Fetch at session start (idempotency check)"
date: 2026-10-15
session_context: "Bumping REV in install-remotion-skill.sh and install-hyperframes.sh on the user's request"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — CLAUDE_PROJECT_DIR=$PWD CLAUDE_CODE_REMOTE=true bash .claude/hooks/install-remotion-skill.sh twice after adding a .rev marker: first run installed 7ba4dcf (3.7 s), second run exited (0.05 s)"
---

**Issue:** Step 4b tells the hook to "exit early when the skill is already present (idempotent)". Both fetch hooks (remotion, hyperframes) did exactly that with `[ -f "$DEST/SKILL.md" ] && exit 0`, so bumping `REV` changed nothing on any machine or session where the skill was already there — the old version stayed installed while the file claimed the new one.

**Suggested improvement:** In Step 4b, make the idempotency check version-aware: after copying, write `$REV` into `<skill>/.rev`, and skip only when `.rev` equals `REV`. Add to Step 5: after a REV bump, run the hook and check `.rev`.

**Principle:** An idempotency check must compare the installed version with the wanted one, not just test for presence; a presence check turns every pinned-version bump into a silent no-op.
