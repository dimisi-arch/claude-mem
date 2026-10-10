#!/bin/bash
# Inject the carried-over session notes and the task-observer start-up
# instruction into every new session, so neither depends on CLAUDE.md being
# read and followed.
set -euo pipefail

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
notes="$root/.claude/context/session-notes.md"

python3 -I - "$root" "$notes" <<'PY'
import json, os, sys

root, notes = sys.argv[1], sys.argv[2]
parts = [
    "Session start (from .claude/hooks/session-start.sh):",
    "- Answer the user in German.",
    "- Before the first other tool call, invoke the `task-observer` skill and run "
    "its Session Start Protocol. Workspace: "
    f"{root}/.claude/task-observer. Step 2 (the log scan) is one command: "
    f"bash {root}/.claude/skills/task-observer/scripts/session-start-scan.sh {root}/.claude/task-observer",
]
if os.path.isfile(notes):
    with open(notes, encoding="utf-8") as f:
        parts.append("\nCarried-over notes (.claude/context/session-notes.md):\n\n" + f.read())
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(parts),
    }
}))
PY
