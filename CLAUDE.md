# Claude-Mem: AI Development Instructions

Claude-mem is a Claude Code plugin providing persistent memory across sessions. It captures tool usage, compresses observations using the Claude Agent SDK, and injects relevant context into future sessions.

## Build

```bash
npm run build-and-sync        # Build, sync to marketplace, restart worker
```

## File Locations

- **Source**: `<project-root>/src/`
- **Built Plugin**: `<project-root>/plugin/`
- **Installed Plugin**: `~/.claude/plugins/marketplaces/thedotmack/`
- **Database**: `~/.claude-mem/claude-mem.db`
- **Chroma**: `~/.claude-mem/chroma/`

## Requirements

- **Bun** (all platforms - auto-installed if missing)
- **uv** (all platforms - auto-installed if missing, provides Python for Chroma)
- Node.js

## Documentation

**Public Docs**: https://docs.claude-mem.ai (Mintlify)
**Source**: `docs/public/` - MDX files, edit `docs.json` for navigation
**Deploy**: Auto-deploys from GitHub on push to main

## Important

No need to edit the changelog ever, it's generated automatically.

## Carried-over session state

Read `.claude/context/session-notes.md` at the start of every session: it holds the user's preferences (answer in German) and the shared open work (Make, Notion rules, tools). The two projects live in private repos: restaurant work in `dimisi-arch/omonia-assistent`, the YouTube channel in `dimisi-arch/age-of-geschichte`; keep their details out of this public repo. Update it before a session ends when that state changes, and keep it under ~9,000 characters: the start hook injects it in full, so move finished topics to `.claude/context/session-notes-archive.md`.

## Always-on rules from the start hook

`.claude/hooks/session-start.sh` also injects two standing rules (user's decisions 2026-10-14): the `i-have-adhd` ruleset, on in every session until the user says "stop adhd mode", and the Notion check (open Chat-Archiv entries, once per session, at most three lines to the user). When the hook did not fire, read `.claude/skills/i-have-adhd/SKILL.md` and the hook's Notion line yourself and follow both.

## Task Observer (skill improvement)

At the start of every session that involves tool calls, invoke the `task-observer` skill (`.claude/skills/task-observer/`) and run its Session Start Protocol before planning or exploring; it stays active for the whole session (user's decision 2026-10-14, reversing the end-only rule tried earlier that day). Step 2 (the log scan) is one command, never a hand-made `ls`: `bash /home/user/claude-mem/.claude/skills/task-observer/scripts/session-start-scan.sh /home/user/claude-mem/.claude/task-observer`. Keep the user informed: each time an observation is written, tell the user in one line what was logged, and end the session with the grouped summary. The hook `.claude/hooks/observer-nudge.sh` adds a reminder on every fourth user message. Reviews run twice a week through the routine "Skill-Verbesserung (Mo + Do)".

- **Workspace (pinned, never derived from the cwd):** `/home/user/claude-mem/.claude/task-observer`
  - Log: `.../skill-observations/observation-log/`
  - Principles: `.../skill-observations/cross-cutting-principles.md`
  - Staged skill updates: `.../skill-updates/` (manifest `PENDING.md`)
- **New observation files** are created only via `bash /home/user/claude-mem/.claude/skills/task-observer/scripts/new-observation.sh <slug> /home/user/claude-mem/.claude/task-observer`.
- **Repositories root:** `/home/user`
- **Other machine:** the paths above are the cloud container's. On the user's Windows PC the same workspace is `C:\Users\Stilianos\claude-mem\.claude\task-observer` (Git Bash: `/c/Users/Stilianos/claude-mem/.claude/task-observer`); replace the `/home/user/claude-mem` root in every command above with that one there.
- The observer only proposes changes; installed skills are changed only after the user approves them in a review.
- Cloud sessions run in throwaway containers: commit and push changes under `.claude/task-observer/` before the session ends, or the observations are lost.

## Session-start hooks may not fire

The SessionStart hooks in `.claude/settings.json` only run when this repo is the session's project. If `.claude/skills/remotion-best-practices/SKILL.md` or the `graphify` command is missing, run them by hand:
`CLAUDE_PROJECT_DIR=/home/user/claude-mem bash .claude/hooks/install-remotion-skill.sh` and `CLAUDE_PROJECT_DIR=/home/user/claude-mem bash .claude/hooks/install-graphify.sh` (from the repo root; replace the path if the repo lives elsewhere). If `agent-reach` or `mcporter` is missing, also run `CLAUDE_PROJECT_DIR=/home/user/claude-mem CLAUDE_CODE_REMOTE=true bash .claude/hooks/install-agent-reach.sh` (installs in the background, ~1 min). If `.claude/skills/hyperframes/SKILL.md` is missing, run `CLAUDE_PROJECT_DIR=/home/user/claude-mem CLAUDE_CODE_REMOTE=true bash .claude/hooks/install-hyperframes.sh`. If `.claude/skills/free-resources/lists/` is empty, run `CLAUDE_PROJECT_DIR=/home/user/claude-mem CLAUDE_CODE_REMOTE=true bash .claude/hooks/install-free-lists.sh`. The graphify hook also builds `graphify-out/` in the background (~2 min) when it is missing.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
