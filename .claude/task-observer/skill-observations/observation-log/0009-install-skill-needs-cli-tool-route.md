---
id: 9
title: "install-third-party-skill has no route for skills that need a CLI tool installed"
status: open
type: internal
skill: [install-third-party-skill]
proposes_skill: []
target_file: []
siblings_checked: "none — install-third-party-skill belongs to no family in this install (no skill-families.md)"
area: "Step 4 (4a/4b) and Step 5 test"
date: 2026-10-10
session_context: "Evaluating and installing Agent Reach (MIT skill plus Python CLI plus mcporter/Exa MCP) for cloud sessions"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — uv tool install --with-executables-from yt-dlp git+https://github.com/Panniantong/Agent-Reach@94f06c1 (worked; without the flag yt-dlp stayed off PATH); npm install -g mcporter && mcporter config add exa https://mcp.exa.ai/mcp --scope home (worked)"
---

**Issue:** The skill covers two routes for the skill *folder* (copy vs. fetch at start), but Agent Reach is a skill whose commands call a CLI (`agent-reach`, `yt-dlp`, `mcporter`). Step 4a copied the folder fine, yet the skill was useless in a fresh container without the tools. The install hook had to be improvised from `install-graphify.sh`: idempotency check per tool, pinned git commit, background install, failure notes to a log file (a backgrounded subshell's stderr otherwise vanishes into /dev/null — first draft lost them). Also, `uv tool install` exposes only the package's own entry points, so a bundled dependency CLI (yt-dlp) needs `--with-executables-from`. Second gap: upstream's skill description said "MUST USE" for every web lookup, which would override the built-in tools and connectors; the skill says "copy unchanged" and gives no rule for when editing the description is justified.

**Suggested improvement:** Add a Step 4c "Skill needs a CLI": a hook on the graphify pattern that pins the tool to the same commit as the copied skill, checks each tool separately, installs in the background, logs failures to a file, and uses `--with-executables-from` for bundled CLIs. In Step 5, test that each command the skill's quick-reference names is on PATH. In Step 4a, allow narrowing an over-broad `description` (record it in SOURCE.md) when it would push aside installed tools.

**Principle:** A skill is only installed when everything its instructions call is reachable in the target environment; verify the commands the skill names, not just that the skill file loads.
