---
name: "install-third-party-skill"
description: "Internal skill for this repo (claude-mem, used from cloud sessions). Use when the user wants a skill, plugin or skill collection from someone else's GitHub repo available in Claude Code — 'install X', 'add the X skill', 'can we use X', or a bare skill/plugin name or repo URL. Covers: finding the upstream skill, license check against this public repo, choosing between committing a copy and fetching it at session start, pinning a version, wiring a SessionStart hook that never fails, testing, and recording the source. Not for writing a new skill from scratch (use skill-creator) or for MCP connectors."
---

# Install a third-party skill (internal)

Internal working skill for `dimisi-arch/claude-mem`. The user is not a
developer: explain each decision in plain German, give copy-paste commands,
and ask before anything that is hard to undo or that publishes content.

## Why this skill exists

Cloud sessions start in a fresh container. `/plugin` and `/skills` do not
work there, and `claude plugin install` only lasts for the running container.
A skill is available in every session only if it is either committed under
`.claude/skills/` or downloaded again at every session start.

## Step 1 — Clarify the ask

A bare name ("remotion-best-practices") can mean "install it" or "use it".
If the skill is not installed yet, ask in one line which one is meant.

## Step 2 — Find the upstream skill

1. Clone the upstream repo into the scratchpad, never into the repo:
   `git clone --depth 1 <url> <scratchpad>/upstream-<name>`.
2. Look for skills under `skills/`, `.claude/skills/`, `agent-skill/`, or
   plugin folders (`.claude-plugin/`, `plugins/*/skills/`). Many projects
   ship their own skill; prefer it over writing one.
3. List the skills found with a one-line purpose and size each. If there are
   many, let the user pick (example: 7 of 25 agent-skills were chosen).
   Leave out on purpose: overlaps with installed skills, skills that fire on
   every change or at every session start, hooks and scripts unless the user
   wants them.
4. Note the commit SHA you looked at: `git -C <clone> rev-parse HEAD`.

## Step 3 — License check (decides everything else)

This repo is **public**. Read the upstream LICENSE file and the skill folder
itself (a folder can carry its own license that differs from the repo).

| License found | Route |
|---|---|
| MIT, Apache 2.0, BSD, CC BY | **Copy and commit** (Step 4a), keep the license file |
| No license, "source-available", custom terms (e.g. Remotion License) | **Ask the user.** Default offer: **fetch at session start** (Step 4b), folder gitignored, nothing republished |
| Terms forbid redistribution or automated download | Do not install; tell the user why |

Say it plainly, e.g. "Diese Lizenz erlaubt kein freies Weitergeben. Ich lade
den Skill deshalb bei jedem Start neu herunter, statt ihn in dein
öffentliches Repo zu kopieren."

## Step 4a — Copy and commit

1. Copy each chosen skill folder to `.claude/skills/<name>/` unchanged.
2. Add the license file next to `SKILL.md` and a `SOURCE.md`:
   `Source: <url> (commit <sha>), <license>.` plus one line on what was
   left out and why.
3. `.claude/skills/` is gitignored in this repo: new skills need
   `git add -f .claude/skills/<name>`.

## Step 4b — Fetch at session start

1. Add `.claude/skills/<name>/` to `.gitignore` with a comment naming the
   license and the hook.
2. Write `.claude/hooks/install-<name>.sh` on the pattern of
   `.claude/hooks/install-remotion-skill.sh`:
   - only runs when `CLAUDE_CODE_REMOTE=true`;
   - exits early when the skill is already present (idempotent);
   - pins one commit (`REV=<sha>`, with a comment naming the version);
   - `git init` + `git fetch --depth 1 <url> "$REV"` with a `timeout`;
   - copies only the skill folder into place;
   - **always ends with `exit 0`** — a failed download prints one line to
     stderr and never blocks the session start.
3. Register it under `hooks.SessionStart` in `.claude/settings.json` with a
   `timeout`. Edit the JSON by hand; never reformat the whole file.

## Step 5 — Test

1. Run the hook by hand twice:
   `CLAUDE_PROJECT_DIR=/home/user/claude-mem CLAUDE_CODE_REMOTE=true bash .claude/hooks/install-<name>.sh`
   — the first run installs, the second must do nothing.
2. Check the result: `SKILL.md` exists and the skill shows up in the skill
   list.
3. Actually use the skill once on a tiny example (Remotion: render a short
   test video). Being in the list does not prove it works.
4. Known gap: hooks only fire when this repo is the session's project.
   `CLAUDE.md` ("Session-start hooks may not fire") holds the manual
   fallback — add the new hook's command there too.

## Step 6 — Record and ship

1. Add a short section to `.claude/context/session-notes.md`: source URL,
   version/commit, license, route (copied or fetched), what was left out.
2. Commit on a `claude/...` branch, push, and open a PR only when the user
   asks. Remind the user that only a merge into `main` makes the skill
   available in new sessions.

## Pre-flight before reporting done

- [ ] License read and route matches the table in Step 3
- [ ] Commit SHA pinned (hook) or recorded in `SOURCE.md` (copy)
- [ ] Hook exits 0 on failure, is idempotent, was run twice
- [ ] Skill used once on a real example
- [ ] CLAUDE.md fallback line updated (fetch route only)
- [ ] session-notes.md updated; branch pushed
