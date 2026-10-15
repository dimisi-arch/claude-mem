---
id: 19
title: "check-claude-setup.sh fails locally on third-party skills fetched at session start (hyperframes), though CI is green"
status: open
type: internal
skill: []
proposes_skill: []
target_file: [".claude/scripts/check-claude-setup.sh"]
siblings_checked: "none — the target is a repo script, not a skill"
area: "Setup check, skill validation pass"
date: 2026-10-15
session_context: "Merging PR #29; the local setup check exited 1"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — bash .claude/scripts/check-claude-setup.sh: exit 1, FAIL for faceless-explainer, general-video, hyperframes-audio, hyperframes-cli, hyperframes-creative (29 'cited path missing' / 'heading not in its own Contents index' lines); all are gitignored folders written by .claude/hooks/install-hyperframes.sh"
---

**Issue:** The setup check runs the bundle validator over every folder in `.claude/skills/`, including third-party skills that a start hook fetches into gitignored folders. Upstream's HyperFrames skills do not follow task-observer's authoring rules (contents indexes, cited paths), so the check fails in every session where the hook ran, while GitHub CI (no fetched folders) stays green. A failing check that is always red teaches the reader to ignore it.

**Suggested improvement:** Skip folders that are gitignored (`git check-ignore -q`) or carry a `.rev` marker from a fetch hook, or validate them only for "SKILL.md exists and frontmatter parses".

**Principle:** A health check should only judge what the repository owns; foreign content fetched at runtime gets a presence check, or the check is red by default and stops meaning anything.
