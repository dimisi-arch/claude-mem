---
id: 21
title: "install-third-party-skill: pin skills that drive a CLI to the released tag, and let size (not only license) pick the fetch route"
status: open
type: internal
skill: [install-third-party-skill]
proposes_skill: []
target_file: []
siblings_checked: "none — no skill-families.md in this install; install-third-party-skill has no sibling skill"
area: "Step 2.4 (note the commit SHA) and Step 3 (license route table)"
date: 2026-10-13
session_context: "Installing HyperFrames skills (heygen-com/hyperframes) after a user asked to install the useful tools from an Instagram reel"
parked_until:
resolved:
resolution:
reference: ".claude/hooks/install-hyperframes.sh (PR #37)"
commands_verified: "run — npx -y hyperframes@0.8.152 init: npm ETARGET (HEAD's package.json version not published); npm view hyperframes version: 0.8.151; git ls-remote --tags: v0.8.151 = 945c61eb; init/check/render with 0.8.151 passed"
---

**Issue:** Two gaps showed up while installing HyperFrames.
1. Step 2.4 says "note the commit SHA you looked at" (the clone's HEAD). For
   a project whose skills drive its own CLI, HEAD was one version ahead of
   npm: the skills' commands (`npx hyperframes@<pin>`) would mismatch the
   published CLI, and `npx hyperframes@0.8.152` failed with ETARGET. The fix
   was pinning to the release tag matching `npm view <pkg> version`.
2. Step 3 picks the route by license only. Apache 2.0 says "copy and
   commit", but the chosen set was ~6 MB across 14 folders; committing that
   to the public repo is heavy, so the fetch route was taken anyway. The
   skill does not mention size as a reason.

**Suggested improvement:** Step 2.4: "If the skills call the project's own
CLI or package, pin the release tag whose version matches the published
package (`npm view <pkg> version`, `git ls-remote --tags`), not HEAD."
Step 3: add a line "Permissive license but large (over ~1 MB) or many
folders → fetch at session start is fine too; say why in the hook comment."
Also mention sparse checkout (`--filter=blob:none` + `sparse-checkout set`)
in Step 4b for big monorepos (70 MB repo → 2 s fetch).

**Principle:** When a skill bundle and a tool release travel together, pin
the bundle to the tool's released version, not the repository tip; and pick
the delivery route by both licence and weight.
