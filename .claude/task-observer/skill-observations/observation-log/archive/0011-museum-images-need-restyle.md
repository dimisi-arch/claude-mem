---
id: 11
title: "historical-images delivered raw museum images; the channel needs them redrawn in its own style"
status: actioned
type: internal
skill: [historical-images]
proposes_skill: []
target_file: []
siblings_checked: "none — historical-images belongs to no family; no skill-families.md in this install"
area: "historical-images workflow, step after choosing images"
date: 2026-10-10
session_context: "Building the historical-images skill for the YouTube channel; the user reviewed the first results"
parked_until:
resolved: 2026-10-10
resolution: "Added step 5 'Restyle into the channel look' to .claude/skills/historical-images/SKILL.md (Canva generate-image with the museum image as reference, Runway alternative with the series-bible style reference, the current style prompt, fixed series rules, AI-content credit note) on the user's request in the same session."
reference:
commands_verified: "run — Canva create-upload-url + POST, generate-image with imageReferences (2 tests, both SUCCESS); a local OpenCV 'graphic novel' filter was tried first and rejected as looking like a cheap photo filter"
---

**Issue:** The skill was built to deliver authentic public-domain images as they are. The user's actual need: the channel has a fixed look (Notion series bible: graphic novel, bold ink, Mediterranean palette), and raw paintings or engravings break it. The user wants them "more drawn, friendlier, less natural", later lightly animated. The skill was designed from the data source outward (what museums offer) instead of from the deliverable inward (what a finished Short needs), and the series bible that states the look was not read before building.

**Suggested improvement:** Done for this skill (step 5). For future content skills: read the project's style/series rules before designing the workflow, and treat sourced material as input to the house style, not as the output.

**Principle:** A skill that feeds a creative product must end in the product's house style; read the style guide first and design backwards from the finished deliverable.
