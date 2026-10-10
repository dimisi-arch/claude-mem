Source: https://github.com/anthropics/claude-plugins-official, plugin `claude-code-setup` v1.0.0 (commit b8e53f1c05dff3b6d751297f6527990ffc81c2f4), Apache License 2.0 (see LICENSE).

Copied unchanged: `skills/claude-automation-recommender/` (SKILL.md and references/).
Left out: the plugin wrapper (`.claude-plugin/plugin.json`, README, example screenshot) — cloud
sessions cannot install plugins, so the skill folder is committed directly.
The skill is read-only: it recommends hooks, skills, MCP servers and subagents but changes nothing.
