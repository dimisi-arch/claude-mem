---
id: 6
title: "Scheduled cloud runs start without the repository, and a prompt that names a tool loosely gets a skipped step"
status: open
type: open-source
skill: [task-observer]
proposes_skill: []
target_file: []
siblings_checked: "none — task-observer belongs to no family in this install (no skill-families.md)"
area: "references/environments.md, scheduled-task prompt rules"
date: 2026-10-10
session_context: "Registering the weekly review as a cloud routine (fresh session per firing); two test firings failed at step 0 before the third"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — fire_trigger test firings 1 and 2: /home/user/claude-mem absent; ToolSearch 'select:add_repo' returned no match although the session's tool list held mcp__claude-code-remote__add_repo"
---

**Issue:** The weekly review was registered as a cloud routine that starts a
fresh session per firing. Firing 1: the session had no repository checked
out, so the pinned workspace path did not exist. The prompt was fixed to
attach and clone the repo first. Firing 2: the prompt said "call the
`add_repo` tool"; the session searched for the bare name, found nothing
(the real name carries a server prefix), and stopped as instructed. Only
the skill's existing rule "setup is not done until one firing has reached
the workspace from inside the task's own execution context" caught both;
an interactive test would have passed.

**Suggested improvement:** In environments.md (scheduled-task prompt
rules), add two lines: (1) a scheduled run may start with no checkout at
all; its prompt's first action obtains the workspace, with a stated
fallback; (2) every tool a scheduled prompt names is named exactly as the
target session lists it (full prefixed name), never a short form.

**Principle:** A prompt for an unattended run is read literally by a
session with a different tool list and filesystem; name tools by their
exact identifiers, give every acquisition step a fallback, and prove the
setup with a real firing.
