#!/bin/bash
# Install the tools the agent-reach skill calls in cloud sessions, which start from a fresh container:
# the agent-reach CLI (brings yt-dlp and feedparser) and mcporter with the free Exa search MCP.
# Agent Reach is MIT (https://github.com/Panniantong/Agent-Reach); the skill itself is committed
# under .claude/skills/agent-reach/. Never fails the session start: a failed install only prints a note.

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

# v1.5.0 (2026-10-08). Bump together with .claude/skills/agent-reach/ (see its SOURCE.md).
REV=94f06c1969dfc1834001269d79d3ad0972d9dee6

need_cli=1; need_exa=1
command -v agent-reach >/dev/null 2>&1 && need_cli=0
command -v mcporter >/dev/null 2>&1 && mcporter config list 2>/dev/null | grep -q exa && need_exa=0
[ "$need_cli$need_exa" = "00" ] && exit 0

# ~1 min in total: run in the background so the start is not held up.
(
  if [ "$need_cli" = 1 ]; then
    timeout 300 uv tool install --with-executables-from yt-dlp "git+https://github.com/Panniantong/Agent-Reach@$REV" >/dev/null 2>&1 \
      || echo "agent-reach install failed; run: uv tool install --with-executables-from yt-dlp git+https://github.com/Panniantong/Agent-Reach@$REV" >&2
  fi
  if [ "$need_exa" = 1 ]; then
    { command -v mcporter >/dev/null 2>&1 || timeout 180 npm install -g mcporter >/dev/null 2>&1; } \
      && timeout 30 mcporter config add exa https://mcp.exa.ai/mcp --scope home >/dev/null 2>&1 \
      || echo "mcporter/Exa setup failed; run: npm install -g mcporter && mcporter config add exa https://mcp.exa.ai/mcp --scope home" >&2
  fi
) </dev/null >/dev/null 2>>"$HOME/.agent-reach-install.log" &
echo "agent-reach tools install started in the background (failures: ~/.agent-reach-install.log)" >&2
exit 0
