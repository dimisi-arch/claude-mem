#!/bin/bash
# Inject the carried-over session notes, the standing session rules and the
# i-have-adhd ruleset into every new session, so none of them depends on
# CLAUDE.md being read and followed.
set -euo pipefail

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
notes="$root/.claude/context/session-notes.md"

python3 -I - "$root" "$notes" <<'PY'
import json, os, re, sys

root, notes = sys.argv[1], sys.argv[2]
archive = "collection://0f9aa644-8d33-447f-b637-7956de2e7e36"
parts = [
    "Session start (from .claude/hooks/session-start.sh):",
    "- Answer the user in German.",
    "- task-observer is active for the whole session again (user's decision "
    "2026-10-14, reversing the end-only rule tried earlier that day). Before the "
    "first other tool call, invoke the `task-observer` skill and run its Session "
    f"Start Protocol. Workspace: {root}/.claude/task-observer. Step 2 (the log scan) is one command: "
    f"bash {root}/.claude/skills/task-observer/scripts/session-start-scan.sh {root}/.claude/task-observer. "
    "Keep the user informed: each time an observation file is written, tell the "
    "user in one German line what was logged (number and topic), and close the "
    "session with the grouped summary. The observer only proposes: skills "
    "change only after the user approves.",
    "- Notion check, once per session with the first answer (user's request "
    "2026-10-14): one notion-query-data-sources call in sql mode on "
    f'{archive}: SELECT "Titel", "date:Datum:start" AS Datum, "Offene Punkte", url '
    f'FROM "{archive}" WHERE "Status" = \'Offen\' ORDER BY "date:Datum:start" DESC LIMIT 10. '
    "Set entries to Erledigt whose open points are done, and tell the user in at "
    "most three lines what is still open. Before the session ends, check that "
    "this session's Chat-Archiv and Code-Sammlung entries exist.",
]
# Always-on ADHD mode: the skill is user-invoked only, so its ruleset is injected here.
adhd = os.path.join(root, ".claude", "skills", "i-have-adhd", "SKILL.md")
if os.path.isfile(adhd):
    with open(adhd, encoding="utf-8") as f:
        body = re.sub(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*\r?\n", "", f.read(), count=1, flags=re.S)
    parts.append(
        "\nADHD MODE ACTIVE (always-on, user's decision 2026-10-14). The ruleset "
        'below applies to every response; "stop adhd mode" turns it off for this '
        "session.\n\n" + body.strip()
    )
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
