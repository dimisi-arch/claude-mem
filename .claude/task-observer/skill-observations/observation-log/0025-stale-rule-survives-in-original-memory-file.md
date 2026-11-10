---
id: 25
title: "Changed rule recorded as a new index line while the original memory file kept the old rule"
status: open
type: internal
skill: []
proposes_skill: []
target_file: ["project memory (private restaurant project): one file per rule subject"]
siblings_checked: "none — target is a project memory store, not a skill; belongs to no skill family"
area: "project memory upkeep when the user changes an existing rule"
date: 2026-11-10
session_context: "Learning pass over one day of guest-mail threads in the private restaurant project (details in that private repo's memory, not here)"
parked_until:
resolved:
resolution:
reference:
commands_verified: none
---

**Issue:** The user reversed a standing rule (an item that used to go into every offer was banned). The thread that received the correction added a new line to the memory index, but the original subject file still stated the old rule in bold as an instruction. Threads that loaded the subject file kept writing the banned item into drafts and offer PDFs the same day; the user had to strike it by hand twice more. The same pass found a second stale source: a session-notes file still describing the old offer template with the banned items "included". A third rule (a waiting-period threshold) was tightened in chat while the file's name and description still carried the old number.

**Suggested improvement:** When a user correction changes an existing rule, the correction is written INTO the file that holds that rule (strike the old text, date the new one), and every other durable copy found by a grep for the rule's keyword is fixed in the same turn (index line, checklist, session notes, templates). A new index line alone is never the carrier of a reversal. Consider a one-line grep step in the project's checklist: "rule changed → grep memory + notes + templates for the keyword".

**Principle:** A reversed rule must be edited where the old rule lives, not appended elsewhere: readers load the subject file, and an addition that does not touch the original leaves two contradictory instructions, of which the older and more detailed one usually wins.

**Instance evidence (same day):** two offer PDFs built before the correction still carried the banned item and went out to the guest; the check that found it was a plain text grep of the PDFs during this learning pass.
