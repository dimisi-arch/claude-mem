---
id: 8
title: "A workspace pinned as one machine's absolute path does not resolve when the same repo is checked out on a second machine"
status: open
type: open-source
skill: [task-observer]
proposes_skill: []
target_file: ["CLAUDE.md"]
siblings_checked: "none — task-observer belongs to no family in this install (no skill-families.md)"
area: "references/environments.md, anchoring the workspace; activation block in CLAUDE.md"
date: 2026-10-10
session_context: "Setting up the user's Windows PC as a second workbench for a repo so far used only from Linux cloud containers"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — session-start-scan.sh and new-observation.sh with /c/Users/Stilianos/claude-mem/.claude/task-observer under Git Bash: both worked; the pinned /home/user/claude-mem/.claude/task-observer does not exist on this machine"
---

**Issue:** The activation block in `CLAUDE.md` pins the workspace and both
script commands to `/home/user/claude-mem/...`, the cloud container's path.
The workspace is committed inside the repository, so on the Windows checkout
(`C:\Users\Stilianos\claude-mem`) the same workspace exists under another
absolute path. The session had to translate the path by hand; a literal run
of the pinned command would have hit the guard for a missing directory, or
on a different script an empty, clean-looking backlog.

**Suggested improvement:** In `references/environments.md` ("Anchoring the
workspace"), cover the case of a workspace that travels with a repository
checked out on several machines: pin it relative to the repository root
(resolved once, e.g. `git rev-parse --show-toplevel`) and state that the
absolute form is derived per machine. The CLAUDE.md block here would name
both known roots or the repo-relative form.

**Principle:** "Absolute" protects against a wrong working directory, not
against a second machine: when the workspace lives inside a versioned
repository, the stable anchor is the repository root, and the absolute path
is derived from it on each machine rather than written down once.
