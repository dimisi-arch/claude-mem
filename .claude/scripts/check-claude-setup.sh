#!/bin/bash
# Checks the committed Claude Code setup: skills, hooks, settings and the
# session notes the start hook injects. Run locally or in CI; exit 1 on any failure.
set -u
export PYTHONDONTWRITEBYTECODE=1
root="$(cd "$(dirname "$0")/../.." && pwd)"
v="$root/.claude/skills/task-observer/scripts/validate-skill-bundle.py"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
fail=0

python3 -I "$v" --selftest >/dev/null || { echo "FAIL validator selftest"; fail=1; }

for d in "$root"/.claude/skills/*/; do
  n=$(basename "$d")
  [ -f "$d/SKILL.md" ] || continue
  cp -r "$d" "$tmp/$n"   # validate a copy: the live skill is never touched
  out=$(python3 -I "$v" "$tmp/$n" 2>&1) && continue
  # {{now}} in the Make examples is a Make formula, not leftover template text.
  real=$(printf '%s\n' "$out" | sed -n '/^FAIL:/,$p' | grep '^  - ' | grep -vF "unresolved template slot ('{{now}}')")
  [ -z "$real" ] && continue
  echo "FAIL skill $n"; printf '%s\n' "$real"; fail=1
done

python3 -I -c 'import json, sys; json.load(open(sys.argv[1]))' "$root/.claude/settings.json" \
  || { echo "FAIL .claude/settings.json is not valid JSON"; fail=1; }
for h in "$root"/.claude/hooks/*.sh; do
  bash -n "$h" || { echo "FAIL syntax $h"; fail=1; }
done

notes="$root/.claude/context/session-notes.md"
c=$(python3 -I -c 'import sys; print(len(open(sys.argv[1], encoding="utf-8").read()))' "$notes")
[ "$c" -le 9000 ] || { echo "FAIL session-notes.md has $c characters (limit 9000, see CLAUDE.md)"; fail=1; }

[ "$fail" -eq 0 ] && echo "OK: skills, hooks, settings and session notes"
exit "$fail"
