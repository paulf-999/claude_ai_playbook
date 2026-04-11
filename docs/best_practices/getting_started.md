# 🚀 Getting started

Foundational practices for getting consistently good results from Claude Code, from your first session onwards.

See also: [Pro tips for beginners](pro_tips_for_beginners.md) — four quick habits from the Anthropic quickstart guide.

| Practice | Source | Description | Example |
|---|---|---|---|
| 🗺️ Start in plan mode | Anthropic | Open every session in explore-before-act mode — Claude reads and plans before making any changes. | See [`"defaultMode": "plan"`](../../src/claude/settings.json#L30) |
| ✅ Bake verification into the plan | Anthropic | Make testing part of the task itself, not an afterthought. Claude catches mistakes before you see them. | Add to `CLAUDE.md`: `"As part of every plan, confirm the acceptance criteria with me and propose tests that validate the requirements before writing any code."` |
| 🛠️ Skill library | Team | Build a library of slash command skills for recurring multi-step workflows — commit, PR, drafting, scheduling. | See [skills/](../../src/claude/skills/README.md) — example: [`/create_confluence_page`](../../src/claude/skills/create_confluence_page/SKILL.md) |
| 🤖 Sub-agent library | Team | Load focused sub-agents for specific tasks — better-targeted output across design, review, writing, and tooling. | See [agents/](../../src/claude/agents/README.md) — example: [`architect`](../../src/claude/agents/core/architect.md) |
| 🛡️ Guardrail hooks | Team | Hook into the session lifecycle to block destructive commands and track session cost. | [hooks/](../../src/claude/hooks/README.md) — examples: [`claude_prompt_reviewer.py`](../../src/claude/hooks/claude_prompt_reviewer.py), [`claude_session_cost.py`](../../src/claude/hooks/claude_session_cost.py) |
