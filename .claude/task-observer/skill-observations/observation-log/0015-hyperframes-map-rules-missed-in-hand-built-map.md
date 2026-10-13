---
id: 15
title: "Hand-built HyperFrames map broke two rules the maps module states (far-polygon filter, pre-hold hidden state) — caught only by snapshots"
status: open
type: open-source
skill: [motion-graphics]
proposes_skill: []
target_file: []
siblings_checked: "none — no skill-families.md; HyperFrames skills are third-party (fetched), so a fix would be a local note or an upstream report"
area: "motion-graphics/categories/maps/module.md (Determinism hard rules) and the shortcut of skipping the director/builder subagent pipeline"
date: 2026-10-13
session_context: "Building a 9:16 recap map (Troy to Sicily) for the Age of Geschichte channel with HyperFrames, after reading the maps module"
parked_until:
resolved:
resolution:
reference: "dimisi-arch/age-of-geschichte PR #1, folgen/01-odysseus-zyklop/teil-2-rueckblick/make-map.mjs"
commands_verified: "run — hyperframes check passed on the broken build (0 errors) while snapshots showed the whole sea filled as land; after filtering polygons to lon 0..40 / lat 25..50 the snapshot was correct"
---

**Issue:** The maps module says to filter country/land polygons to a lon/lat
box around the subject and to `gsap.set` hidden states because a bare
`fromTo` applies its "from" values. I had read the module, skipped the
director/builder subagent pipeline to build by hand, and still made both
mistakes: Antarctica in `land-10m` turned the whole Mercator frame into land,
and a `fromTo` pulse ring showed from frame 0. `hyperframes check` passed in
both cases (layout and contrast audits do not see a wrong fill or an early
ring); only the snapshot contact sheet revealed them.

**Suggested improvement:** When building a HyperFrames piece by hand instead
of through the workflow, treat `snapshot` + looking at the contact sheet as a
mandatory gate before render, not optional — `check` passing is not visual
correctness. Locally, consider a short checklist note in session notes for
hand-built maps (filter far polygons; `immediateRender: false` or `gsap.set`
for delayed `fromTo`).

**Principle:** A passing structural check says nothing about whether the
picture is right; for visual output, the rules most likely to be missed are
the ones a rendered frame exposes immediately, so look at frames before
declaring done.
