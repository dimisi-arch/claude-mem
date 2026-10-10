# Session notes — archive

Finished or dropped topics moved out of session-notes.md (which is injected
at every session start and must stay short). Read only when a topic comes up.

## OmniRoute (github.com/diegosouzapw/OmniRoute) — DROPPED 2026-10-09

User decided to drop OmniRoute (free `auto` tier refused by OpenCode). Do not
pursue it further unless the user brings it up again. History below.


User wants Claude Code to run through it. Only possible on the user's own
machine (`npm install -g omniroute`, dashboard `localhost:20128`, then
`omniroute launch` or `ANTHROPIC_BASE_URL=http://localhost:20128` without
`/v1` plus `ANTHROPIC_AUTH_TOKEN`). Never set this in a cloud session. Caveats
already explained: code goes to third-party providers, some providers have
risky terms, non-Claude models work worse with Claude Code, ~8 GB RAM.
Offered next: per-project activation or Docker setup.

## task-observer

Installed in `.claude/skills/task-observer/`, activated in `CLAUDE.md`. The
shortened activation was used (the verbatim upstream block was not inserted).

## ponytail (2026-10-08)

Skills from github.com/DietrichGebert/ponytail (MIT) copied into
`.claude/skills/ponytail*` (6 skills, hooks left out), because `/plugin` does
not work in cloud sessions. On branch `claude/ponytail-plugin-install-60yz0p`;
available in every session only once merged into the main branch. Coding only;
not for the restaurant e-mails.

## frontend-design (2026-10-09)

Anthropic's `frontend-design` plugin skill (Apache 2.0) copied into
`.claude/skills/frontend-design/`. In cloud sessions `claude plugin install`
works only for the running container; the official marketplace is named
`anthropic-plugin-directory` here, not `claude-plugins-official`.

## agent-skills by Addy Osmani (2026-10-09)

User chose a selection of 7 of the 25 skills from github.com/addyosmani/agent-skills
(MIT), copied into `.claude/skills/`: idea-refine, interview-me,
planning-and-task-breakdown, spec-driven-development,
debugging-and-error-recovery, security-and-hardening, documentation-and-adrs.
Left out on purpose: overlaps (code review, simplification, frontend) and
skills that fire on every change (TDD, git workflow, using-agent-skills at
session start). Some copied skills mention test-driven-development /
incremental-implementation / observability-and-instrumentation, which are not
installed. Hooks and scripts of that repo not copied.

## graphify (2026-10-09)

User chose the full setup. CLI `graphifyy` (PyPI, double y = official name;
github.com/Graphify-Labs/graphify, MIT/Apache 2.0) is installed at every cloud
session start by `.claude/hooks/install-graphify.sh` (SessionStart, remote
only, never fails the start). `graphify install --project` added the skill
(`.claude/skills/graphify/`), `.claude/CLAUDE.md`, a graphify section in
`CLAUDE.md` and two PreToolUse hooks; the hooks were wrapped so they do
nothing when the CLI is missing. Graph for `src/` built 2026-10-09 (6322 nodes,
215 communities, ~464k tokens for 5 docs + 6 images); `graphify-out/` is
gitignored, so it is lost with the container unless the user asks to commit it.

## Remotion skill (2026-10-09)

`remotion-best-practices` (github.com/remotion-dev/skills, version 4.0.534;
router that bundles all 11 Remotion sub-skills) is fetched at every cloud
session start by `.claude/hooks/install-remotion-skill.sh`, pinned to one
commit (bump `REV` to update). The content is under the Remotion License (no
classic open-source license), so the user decided to keep it out of the public
repo: `.claude/skills/remotion-best-practices/` is gitignored. Intended use:
code-built videos (React), e.g. intros/animations for "Age of Geschichte".

Tested 2026-10-09: rendering works in the cloud (remotion@4.0.534, React 18,
3-second 720p intro rendered in seconds). Must pass
`--browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`
— the normal `/opt/pw-browsers/chromium` fails ("Old Headless mode has been
removed"). Start hooks (Remotion skill, graphify) did NOT run in a session that
started in `/home/user` instead of the repo; fallback:
`CLAUDE_PROJECT_DIR=/home/user/claude-mem bash .claude/hooks/install-remotion-skill.sh`.

## OmniRoute test in the cloud (2026-10-09)

User asked to test `curl localhost:20128/v1/chat/completions` with model
`auto` and open a PR if it works. Result: OmniRoute 3.8.51 installs and starts
(needs Node >= 22.22.2; container has 22.22.0, worked with node@24 from npm),
bound to 127.0.0.1 because the default listens on 0.0.0.0 without an API key.
The request failed: the free `auto` provider opencode.ai is blocked by the
environment's network policy. No PR opened because the test did not pass.
Nothing was routed through it; Claude Code settings untouched.
User's own Windows PC (2026-10-09): OmniRoute 3.8.51 installed and running
(PowerShell 7.6.6 available; npm skipped install scripts but the server still
started). Test with `auto` reached OpenCode, which answered HTTP 403 "free tier
can only be used from within OpenCode" — the README's zero-credential claim no
longer holds. Test not passed, so no PR. Dashboard password was still the
default "CHANGEME"; user told to change it. User pasted an OmniRoute API key in
chat; told to rotate it; not stored anywhere.

## install-third-party-skill (2026-10-09)

Own internal skill in `.claude/skills/install-third-party-skill/` (built from
task-observer observation #2): checklist for adding someone else's skill —
license check against this public repo, copy+commit vs. fetch-at-start hook,
pin a commit, test twice, record source here. First task-observer review ran
2026-10-09 (all 29 starter principles adopted; record in
`.claude/task-observer/skill-observations/reviews/2026-10-09/`).

## Moved from session-notes.md 2026-10-10 (self-improvement loop)

- Upstream's CI (`ci.yml`, `windows.yml`) is skipped in this fork (fork guard
  per job): it was red on main and mailed the user on every push.
- `.claude/scripts/check-claude-setup.sh` checks skills, hooks, settings and
  the notes length; GitHub workflow `claude-setup.yml` runs it (Actions must be
  enabled on the fork).
- task-observer 3.6.0 installed 2026-10-10: its step-2 scan is one command
  (`scripts/session-start-scan.sh`), named in the start hook and CLAUDE.md.

## YouTube channel description (done 2026-10-09, moved 2026-10-10)

Channel description (all eras, "Age of ..." style, German only, no English) set via
Make scenario 7864799 "Kanalbeschreibung setzen (Age of Geschichte)" (inactive; edit
its mapper and run it to change the text) and verified live; banner kept.

## Local PC details (moved 2026-10-10)

- Remotion renders with
  `--browser-executable="C:/Program Files/Google/Chrome/Application/chrome.exe"`.
- Only here (GitHub login via `gh`): playwright-test-results,
  playwright-devops; playwright-dev (needs the build).

## Declined tools

- Headroom (chopratejas/headroom, context compression proxy): declined 2026-10-10 —
  needs Claude Code traffic routed through a local proxy (impossible in cloud sessions),
  installs Serena and edits settings; little gain for e-mail/Make/Notion work.
