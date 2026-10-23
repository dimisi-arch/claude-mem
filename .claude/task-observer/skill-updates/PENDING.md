# Staged skill updates awaiting install

- `2026-10-23-b/install-third-party-skill` (#24): before a REV bump, compare the hook's skill
  list with `git ls-tree` of the new REV; hooks for a skill set remove their own stale folders.
  Bundle check passed. Install: copy the folder over `.claude/skills/install-third-party-skill/`.

(2026-10-23 earlier: installed voice-summary, install-third-party-skill, task-observer 3.7.0,
ponytail, ponytail-debt, ponytail-gain, ponytail-help, impeccable, agent-reach,
documentation-and-adrs, idea-refine, security-and-hardening.)
