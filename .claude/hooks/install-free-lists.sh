#!/bin/bash
# Download three curated lists for the free-resources skill in cloud sessions, which start
# from a fresh container: public-apis (MIT), awesome-mcp-servers (MIT) and free-for-dev (no
# license file, so it is never committed). Only the README of each is fetched, always from
# the default branch: these lists change daily and are read as data, never executed.
# Never fails the session start: a failed download only prints a note.

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
dir="$root/.claude/skills/free-resources/lists"
mkdir -p "$dir"

fetch() { # name owner/repo
  local out="$dir/$1.md"
  [ -s "$out" ] && [ -z "$(find "$out" -mmin +1440)" ] && return 0   # fresh copy (< 1 day): skip
  if timeout 60 curl -fsSL "https://raw.githubusercontent.com/$2/HEAD/README.md" -o "$out.tmp"; then
    mv "$out.tmp" "$out"
  else
    rm -f "$out.tmp"
    echo "free-resources: could not download $2; run: CLAUDE_CODE_REMOTE=true bash .claude/hooks/install-free-lists.sh" >&2
  fi
}

fetch public-apis public-apis/public-apis
fetch awesome-mcp-servers punkpeye/awesome-mcp-servers
fetch free-for-dev ripienaar/free-for-dev
exit 0
