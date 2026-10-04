# 🚀 Getting started

Foundational practices for getting consistently good results from Claude Code, from your first session onwards.

See also: [Pro tips for beginners](pro_tips_for_beginners.md) — four quick habits from the Anthropic quickstart guide.

| Practice | Source | Description | Example |
|---|---|---|---|
| 🗺️ Start in plan mode | Anthropic | Open every session in explore-before-act mode — Claude reads and plans before making any changes. | See [`"defaultMode": "plan"`](../../src/claude/settings.json#L30) |
| ✅ Bake verification into the plan | Anthropic | Make testing part of the task itself, not an afterthought. Claude catches mistakes before you see them. | Add to `CLAUDE.md`: `"As part of every plan, confirm the acceptance criteria with me and propose tests that validate the requirements before writing any code."` |
| 🛠️ Skill library | Team | Build a library of slash command skills for recurring multi-step workflows — commit, PR, drafting, scheduling. | See [skills/](../../src/claude/skills/README.md) — example: [`/confluence_create_page`](../../src/claude/skills/_atlassian_skills/confluence_create_page/SKILL.md) |
| 🤖 Sub-agent library | Team | Load a focused sub-agent for a specific task — better-targeted output, such as drafting PR descriptions and Confluence pages. | See [sub-agents](../reference/claude_config/sub_agents.md) — example: [`technical_writer`](../../src/claude/agents/core/technical_writer/AGENT.md) |
| 🛡️ Guardrail hooks | Team | Hook into the session lifecycle to block badly named config files and inject your response standards every turn. | [hooks](../reference/claude_config/hooks.md) — examples: [`hook_enforcement_naming_convention.sh`](../../src/claude/hooks/hook_enforcement_naming_convention.sh), [`hook_style_guide_response_standards_inject.sh`](../../src/claude/hooks/hook_style_guide_response_standards_inject.sh) |
