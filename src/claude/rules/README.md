# 📏 Rules

Hard rules that Claude must follow across all sessions and projects.

| File / Directory | Purpose |
|------------------|---------|
| [`behaviour/`](behaviour/README.md) | 🛡️ [General conduct](behaviour/README.md) and the explicit list of actions requiring user confirmation |
| [`development.md`](development.md) | 🔧 Development principles: error handling and config-driven design |
| [`documentation.md`](documentation.md) | 📝 Documentation update rules — minimal diff, self-validation checklist, diff-first presentation |
| [`file_standards.md`](file_standards.md) | 🧹 File hygiene enforced on every commit (newlines, whitespace, encoding, no secrets) |
| [`git.md`](git.md) | 🌿 Commit format, branch naming, PR standards, protected branch rules, repo structure, and `.gitignore` management |
| [`security.md`](security.md) | 🔐 Secrets management, dependency security, input validation, and security testing boundaries |
| [`testing.md`](testing.md) | ✅ Test requirements: no task is complete without passing tests; gaps must be surfaced before proceeding |
| [`workflows.md`](workflows.md) | 🔄 Common end-to-end patterns: feature development, bug fix, code review, data pipeline, infrastructure, documentation |
| [`integrations.md`](integrations.md) | 🔌 MCP server discipline — reuse cached results, fetch only what's needed, batch operations |
| [`cost_efficiency.md`](cost_efficiency.md) | 💰 Credit efficiency — avoid redundant tool calls, sub-agent discipline, concise responses |
| [`transparency.md`](transparency.md) | 🔍 Execution transparency — estimate scope upfront, narrate progress, warn before lengthy operations |
| [`optimisation.md`](optimisation.md) | ⚡ Always-on optimisation — parallel by default, no redundant reads, flag inefficiency mid-session |
| [`skill_standards.md`](skill_standards.md) | ✏️ Skill authoring rules — max 100 lines, child pages for long content, emojis required, mandatory frontmatter and scope gate |
| [`managed_files.md`](managed_files.md) | 📋 Managed index files that must not be edited directly — `docs/whats_installed.md`, `src/claude/agents/README.md`, and `src/claude/skills/README.md` |
