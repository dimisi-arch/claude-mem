---
id: 6
title: "Bundle gate's unresolved-slot rule fails a skill whose example data legitimately uses {{…}} syntax"
status: open
type: open-source
skill: [task-observer]
proposes_skill: []
target_file: []
siblings_checked: "none — task-observer belongs to no family in this install (no skill-families.md)"
area: "Delivering updated skills, pre-delivery gate item (7); scripts/validate-skill-bundle.py"
date: 2026-10-10
session_context: "Scheduled weekly review 2026-10-10: staging make-scenario-building for observation #4"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — validate-skill-bundle.py <staged make-scenario-building> --pack … printed FAIL: unresolved template slot ('{{now}}') in examples/webhook-to-google-sheets.json:30, router-fanout.json:50, if-else-merge.json:76"
---

**Issue:** The staged copy of make-scenario-building (one additive paragraph in
SKILL.md) could not be packed: the gate's unresolved-slot rule flagged `{{now}}`
in three example blueprint JSON files. `{{…}}` is Make's mapping language (IML),
so those are real content, not edit residue. The documented waivers (a path
containing `template`, or a first-line `<!-- template: slots intentional -->`
marker) cannot apply: the files are not templates, and JSON cannot carry an
HTML comment. The run had no compliant way to pack the bundle, and hand-packing
is forbidden, so the update was delivered as a staged directory only.

**Suggested improvement:** Give the unresolved-slot rule a waiver that works for
any file type — e.g. a `.slots-intentional` file in the skill root listing
globs, or skipping data files (`*.json`, `*.yaml`) whose `{{…}}` is a known
templating syntax — and document it next to the existing two waivers.

**Principle:** A content heuristic in a delivery gate needs an opt-out usable by
every file type the gate scans; a waiver expressed in one format's comment
syntax leaves the other formats with a choice between a false failure and a
bypass.
