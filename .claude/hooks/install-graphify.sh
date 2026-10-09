#!/bin/bash
# Install the graphify CLI in cloud sessions, which start from a fresh container.
# The graphify skill and its PreToolUse hooks need the `graphify` command.
# Never fails the session start: a failed install only prints a note.

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
command -v graphify >/dev/null 2>&1 && exit 0

if timeout 300 uv tool install graphifyy >/dev/null 2>&1; then
  echo "graphify installed" >&2
else
  echo "graphify install failed; run: uv tool install graphifyy" >&2
fi
exit 0
