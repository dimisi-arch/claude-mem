---
id: 24
title: "A REV bump in a fetch hook silently dropped 9 skills because upstream had folded them into one"
status: open
type: open-source
skill: [install-third-party-skill]
proposes_skill: []
target_file: []
siblings_checked: "none — install-third-party-skill belongs to no family"
area: "Step 4b/5 — updating a pinned REV"
date: 2026-10-23
session_context: "Bumping hyperframes v0.8.159 -> v0.8.186 in .claude/hooks/install-hyperframes.sh"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — git ls-tree -d FETCH_HEAD skills/ at v0.8.186 listed 7 folders; 9 of the hook's 14 names were gone, so the hook re-fetched at every start and kept stale copies"
---

**Issue:** The REV was bumped after a version check only. Upstream had merged its workflow skills into one; the hook's fixed name list then pointed at folders that no longer existed, so it re-downloaded at every start and kept stale copies. Found only while setting up a second repo.

**Suggested improvement:** Step 5 in install-third-party-skill: after a REV bump, compare the hook's skill list with `git ls-tree -d <REV> skills/` and drop or rename entries; the hook should remove folders it installed that are no longer listed.

**Principle:** Bumping a pinned version is a change to the contents, not to a number: diff what the new version actually ships against what you expect before you call the update done.
