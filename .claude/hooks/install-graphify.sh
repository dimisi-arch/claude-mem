#!/bin/bash
# Install the graphify CLI in cloud sessions, which start from a fresh container,
# and build the graph (graphify-out/ is gitignored, so every container lacks it).
# The graphify skill and its PreToolUse hooks need the `graphify` command.
# Never fails the session start: a failed install only prints a note.

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

if ! command -v graphify >/dev/null 2>&1; then
  if timeout 300 uv tool install graphifyy >/dev/null 2>&1; then
    echo "graphify installed" >&2
  else
    echo "graphify install failed; run: uv tool install graphifyy" >&2
    exit 0
  fi
fi

# AST-only, no API cost, ~2 min for the whole repo: run in the background so the start is not held up.
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
if [ ! -f "$root/graphify-out/graph.json" ]; then
  (cd "$root" && nohup graphify update . >/dev/null 2>&1 &)
  echo "graphify graph build started in the background" >&2
fi
exit 0
