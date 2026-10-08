---
id: 1
title: "Make skills name tools the claude.ai Make connector does not expose"
status: actioned
type: open-source
skill: [make-scenario-building, make-scenario-explore, make-scenario-operations, make-scenario-reference]
proposes_skill: []
target_file: []
siblings_checked: "make-scenario family (no registry yet): building, explore, operations, reference — all four added; each SKILL.md names the same tool surface"
area: "tool names throughout the workflow sections"
date: 2026-10-08
session_context: "Onboarding a user to Make via Claude Code cloud session; building three Notion/Gmail scenarios"
parked_until:
resolved: 2026-10-08
resolution: "Mapping table added to make-scenario-reference (\"When the session exposes a different tool set\"); one-line pointer added to building, explore and operations ground rules. User-approved in session."
reference:
commands_verified: none
---

**Issue:** The skills drive a tool surface named `environment_get`, `app_find`,
`module_spec`, `module_field_resolve`, `connection_create`, `scenario_create`,
`scenario_patch`, `scenario_run`. The Make MCP reachable in the session (the
claude.ai Make connector) exposes a different surface: `apps_recommend`,
`app-modules_list`, `app-module_get`, `credential-requests_create`,
`scenarios_create`, `validate_blueprint_schema`, `hooks_create`, … Only
`environment_get` matched. The building workflow had to be translated by hand
at every step, and the skill gave no hint that a second surface exists.

**Suggested improvement:** In each skill's ground rules, add a short check:
"if the named tools are absent, you are on the older Make MCP surface — use
this mapping" (app_find → apps_recommend/app-modules_list, module_spec →
app-module_get, connection_create → credential-requests_create, scenario_create
→ scenarios_create + validate_blueprint_schema). Alternatively state that the
skills require the server at mcp.make.com/claude and tell the user how to add it.

**Principle:** A skill that drives a specific tool surface must name the surface
it was written against and say what to do when the session exposes a different
one; otherwise the agent improvises the translation silently every time.
