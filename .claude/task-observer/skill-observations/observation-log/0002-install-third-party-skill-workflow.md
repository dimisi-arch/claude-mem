---
id: 2
title: "Recurring workflow: installing a third-party skill in cloud sessions (license check, commit vs. fetch-at-start)"
status: open
type: open-source
skill: []
proposes_skill: [install-third-party-skill]
target_file: []
siblings_checked: "none — no existing skill covers installing third-party skills; session-start-hook only covers test/lint setup"
area: "skill installation in ephemeral cloud containers"
date: 2026-10-09
session_context: "User typed only a skill name (remotion-best-practices) that was not installed; fifth third-party skill install in this repo (ponytail, frontend-design, agent-skills, graphify, remotion)"
parked_until:
resolved:
resolution:
reference: ".claude/context/session-notes.md (sections ponytail, frontend-design, agent-skills, graphify, Remotion skill)"
commands_verified: "none"
---

**Issue:** Installing a third-party skill has now happened five times with the
same steps re-derived each time: find the upstream repo, check the license,
decide between copying into .claude/skills/ (committed) and fetching at
session start (gitignored + SessionStart hook), pin a version, record the
source in session notes, push. This time the upstream repo had no LICENSE file
and its content falls under a source-available license, while the target repo
is public, so the decision needed the user. A bare skill name typed as the
whole message was also ambiguous (install vs. use) and needed one question.

**Suggested improvement:** New skill "install-third-party-skill": (1) clone to
scratchpad, list skills and their sizes; (2) license check — permissive →
copy and commit with attribution; none/source-available and public repo →
ask, offer fetch-at-start hook pinned to a commit SHA with the folder
gitignored; (3) hooks never fail session start; (4) test the hook twice
(install + idempotent rerun); (5) keep settings.json formatting intact
(no blanket json.dumps reformat); (6) record source/version in session notes.

**Principle:** When a task type recurs with the same decision points, the
decision points (here: license vs. repo visibility) belong in a skill so they
are asked every time, not rediscovered.
