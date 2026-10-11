#!/usr/bin/env bash
# SessionStart: once a day, switch skills unused for 14 days to name-only
# (see .claude/skills/skill-usage/SKILL.md). Prints one line only when it
# switched something. Never blocks the session start.
ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
SCRIPT="$ROOT/.claude/skills/skill-usage/scripts/skill_usage.py"
[ -f "$SCRIPT" ] || exit 0
for py in python3 python; do
  if command -v "$py" >/dev/null 2>&1 && "$py" -c 'import sys; sys.exit(sys.version_info < (3, 9))' >/dev/null 2>&1; then
    "$py" "$SCRIPT" --project "$ROOT" --apply --daily --quiet 2>/dev/null
    exit 0
  fi
done
exit 0
