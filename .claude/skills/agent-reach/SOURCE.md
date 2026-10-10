Source: https://github.com/Panniantong/Agent-Reach (commit 94f06c1969dfc1834001269d79d3ad0972d9dee6, v1.5.0), MIT License (see LICENSE).

Copied from `agent_reach/skill/`: `SKILL_en.md` as `SKILL.md`, plus `references/` unchanged.
Changed: the `description` (upstream says "MUST USE" for every web lookup, which would push
aside WebSearch, TubeAlfred and the GitHub tools) and an added "Local notes" block.
Left out: the Chinese `SKILL.md` (same content) and upstream's `agent-reach install --system`
skill registration — the CLI comes from `.claude/hooks/install-agent-reach.sh`, pinned to the
same commit.
