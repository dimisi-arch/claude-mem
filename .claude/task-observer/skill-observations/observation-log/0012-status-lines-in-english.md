---
id: 12
title: "Rule 'answer in German' broken in status lines between tool calls and in PR texts"
status: open
type: internal
skill: []
proposes_skill: []
target_file: [".claude/context/session-notes.md", "CLAUDE.md"]
siblings_checked: "none — the rule lives in the session notes and user preferences, not in a skill"
area: "Language of every user-visible text"
date: 2026-10-10
session_context: "Long session evaluating and installing skills; the user follows on the phone and listens to voice summaries"
parked_until:
resolved:
resolution:
reference:
commands_verified: none
---

**Issue:** The user's preference ("Antworte auf Deutsch") and the session notes ("Answer in German") were loaded, and the final replies were German — but the short status lines written between tool calls ("Both repos are empty…", "Making the routine run…"), and all PR descriptions and commit messages, were English. The user reads those lines in the app and reminded: "Vergiss nicht, dass ich Deutsch spreche und nicht Englisch." Protection in play: written down and loaded into context, no checkpoint. Cause: the working language of tool output and code drifts into the narration; the rule was read as "final answer" rather than "every visible text".

**Suggested improvement:** Session notes now say "every message, also the short status lines between tool calls, and PR descriptions on GitHub". If it happens again (second violation), add a structural barrier instead of more wording — e.g. a check in the PR-creation step of the relevant skills or a hook that flags an English PR body for this repo.

**Principle:** A language preference applies to every text the user can see, including progress narration and artefacts they review (PRs, commit messages they read when merging); state the rule with that scope explicitly.
