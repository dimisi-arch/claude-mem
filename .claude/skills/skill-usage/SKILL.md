---
name: skill-usage
description: Internal skill for this repo. Reports which skills were used in the last 7 days (how often, on which days, when last), what each costs in tokens, and switches skills unused for 14 days to name-only to save tokens. Use when the user asks which skills are used or unused, wants a skill inventory or usage list ("Skill-Nutzung", "welche Skills benutzen wir"), or wants to save tokens by switching skills off.
---

# Skill usage (internal)

Internal working skill for `dimisi-arch/claude-mem`. The user is not a developer:
answer in German, plainly. One script does all counting and switching, so a run
costs one command and one table. Do not count by hand or re-read transcripts.

## Report

Run from the repo root (on the PC use Git Bash; `python3` works where `python` is absent):

```bash
python .claude/skills/skill-usage/scripts/skill_usage.py
```

It prints a German report and saves it to `~/.claude/skill-usage/report.md`. Relay
the two tables and the cost lines as they are. Add at most three sentences of your
own: the most used skill, how many are unused, and what was or will be switched.
`--days N` changes the window; the default of 7 is what the user asked for.

What counts as use: a `Skill` tool call, a `/name` command typed by the user, and a
shell command that names `skills/<name>` and runs something under `scripts/`.
Reading or listing a skill's files does not count. A skill used only by following
its text, with no call and no script, is invisible to the count: before a switch
surprises the user, check the "nicht benutzt" table for skills you know were used.

## Limits to state with every report

- Only sessions on the machine the script runs on are counted. Transcripts live in
  `~/.claude/projects/`; cloud sessions keep theirs in the cloud. If the report says
  no transcripts were found, the count is empty, not zero use: say so.
- Token figures are estimates (4 characters ≈ 1 token).
- The line "Datenbasis" names how many days of history exist. With fewer days than
  the window, "nicht benutzt" means "not used since then".

## Switching skills to save tokens

Every installed skill puts its name and description into every session. A skill set
to `name-only` keeps its name there and drops the description, so Claude can still
call it and the user can still type `/name`.

```bash
python .claude/skills/skill-usage/scripts/skill_usage.py --apply
```

`--apply` writes `skillOverrides` entries to `.claude/settings.local.json` (this
machine only, not committed). Without `--apply` the report shows the plan and
changes nothing. The rules are in the script, not here to re-derive:

- to `name-only`: unused for 14 days, installed for 14 days, 14 days of history
  exist, not listed in `protected.txt`, and its description is long enough to matter;
- back to full: a skill this script switched is used again;
- never `off`, and never an entry the script did not set itself.

The start hook `.claude/hooks/skill-usage.sh` runs `--apply --daily --quiet` once a
day and prints one line only when it switched something. A new setting takes effect
in the next session.

Not switchable by this script, because `skillOverrides` does not cover them: plugin
skills and skills synced from claude.ai (names with a prefix such as
`anthropic-skills:` or `design:`). The report still counts their use. If the user
wants those off, they do it in the claude.ai settings or by disabling the plugin.

## When the user asks to switch one by hand

- Keep a skill always on: add its name and a reason to `protected.txt`.
- Switch one back: delete its line under `skillOverrides` in
  `.claude/settings.local.json` and its entry under `managed` in
  `~/.claude/skill-usage/state.json`.
- Switch one fully off (`"off"`): ask first, name what will stop working, then add
  the entry by hand. The script leaves entries it did not set alone.

## Before reporting done

- [ ] The report came from the script, run this turn
- [ ] The three limits above are stated where they apply
- [ ] Every switch named in the reply appears under "Schaltungen" in the report
