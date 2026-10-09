---
id: 4
title: "A target created for a scenario is invisible to the Make connection until it is shared with it"
status: open
type: open-source
skill: [make-scenario-building]
proposes_skill: []
target_file: []
siblings_checked: "make-scenario family: building added; reference excluded (its Scopes section is about token permissions, not per-resource sharing); explore and operations excluded (they read existing scenarios, they do not create targets)"
area: "Build a new scenario, step 5 (Connections)"
date: 2026-10-09
session_context: "Building webhook -> Notion scenario; the Notion database was created via the Notion MCP connector, then Make's Notion connection did not list it"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — rpc listDataSources with the Notion connection returned [] for the new database and listed only the three databases shared earlier"
---

**Issue:** Step 5 says "reuse an id from connection.existing". The existing
Notion connection was valid, but a database created minutes earlier through
another tool (the Notion connector) was not visible to it: OAuth-scoped apps
like Notion grant access per page/database, so a new resource is unshared by
default. Validation of the module passed anyway (map mode takes a raw id), so
the gap would only have shown at the first run.

**Suggested improvement:** In step 5, add: when the scenario writes to a
resource that is new or was created outside Make, list it through the
connection (the module's ID-finder RPC) before building; if it is missing, tell
the user the one sharing step (Notion: ••• → Connections → add the Make
integration) and re-check after they confirm.

**Principle:** A valid connection proves authentication, not access to a
specific resource; check that the connection can see the exact target before
relying on it, because module validation with a raw id does not.
