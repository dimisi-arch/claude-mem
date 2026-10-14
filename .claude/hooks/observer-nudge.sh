#!/bin/bash
# UserPromptSubmit hook: every 4th user message, remind Claude to flush task-observer
# observations. The user asked (2026-10-10) for the observer to be more active; a remembered
# "log it later" is exactly what task-observer says gets lost, so the reminder is structural.
# Prints nothing on the other prompts. Never blocks a prompt.

input=$(cat)
sid=$(printf '%s' "$input" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
counter="${TMPDIR:-/tmp}/claude-observer-nudge-${sid:-default}"
n=$(( $(cat "$counter" 2>/dev/null || echo 0) + 1 ))
echo "$n" > "$counter" 2>/dev/null

if [ $(( n % 4 )) -eq 0 ]; then
  echo "task-observer checkpoint (message $n): before answering, write any pending observation from the last few turns — user corrections, a rule you broke, a workaround you needed, a workflow worth a skill — with .claude/skills/task-observer/scripts/new-observation.sh, or append a one-line 'no observations' to .claude/task-observer/skill-observations/checkpoints.log."
fi
exit 0
