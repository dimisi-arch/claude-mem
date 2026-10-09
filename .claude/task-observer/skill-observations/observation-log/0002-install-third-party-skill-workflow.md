---
id: 2
title: "Recurring workflow: installing a third-party skill in cloud sessions (license check, commit vs. fetch-at-start, hook may not fire)"
status: open
type: open-source
skill: []
proposes_skill: [install-third-party-skill]
target_file: []
siblings_checked: "none — no existing skill covers installing third-party skills; session-start-hook only covers test/lint setup"
area: "skill installation in ephemeral cloud containers"
date: 2026-10-09
session_context: "Two sessions on 2026-10-09: (1) user typed only a skill name (remotion-best-practices) that was not installed; fifth third-party skill install in this repo (ponytail, frontend-design, agent-skills, graphify, remotion); (2) Remotion check found the start hook had not fired"
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

**Instance 2026-10-09 (later session, "Funktioniert remotion?"):** the
fetch-at-start hook had not run. The session started with `/home/user` as its
working directory (several repos side by side), `CLAUDE_PROJECT_DIR` was empty,
and neither the Remotion skill nor the graphify CLI was present — both hooks
live in `claude-mem/.claude/settings.json`, which only fires when that repo is
the session's project. Step (4) above tested the hook by running it by hand,
which cannot catch this. Added step: (7) the fetch-at-start choice depends on
the hook actually firing; verify in a fresh session that the skill exists, and
tell the user the fallback (run the hook by hand) when the repo is not the
session's project.

**Review 2026-10-09:** step (7)'s fallback is applied — `CLAUDE.md` section
"Session-start hooks may not fire". The new skill itself is still open; the
user did not choose to build it in this review.

**Principle:** When a task type recurs with the same decision points, the
decision points (here: license vs. repo visibility) belong in a skill so they
are asked every time, not rediscovered.
