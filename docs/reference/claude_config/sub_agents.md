# 🤖 Sub-agents

Sub-agents are specialist personas that shape how Claude behaves in a session — what role it plays, what priorities it applies, and how it frames its responses. Each agent runs in its own context window with a focused system prompt, specific tool access, and independent permissions.

---

## 📋 Available agents

See [`src/claude/agents/`](../../../src/claude/agents/) — the folder is the current list, grouped by domain folder.

- **Example:** [`technical_writer`](../../../src/claude/agents/core/technical_writer/AGENT.md) drafts PR descriptions and Confluence page text as local files, and never publishes them.
- **Adding one:** follow `authoring_agents.md` in `src/claude/_rules/03_authoring_guidelines/`.

---

## 🚀 Using an agent

- **By name:** ask Claude to use it, e.g. "use the technical_writer agent to draft the PR body".
- **By trigger:** each agent's `triggers:` frontmatter lists the phrases that route work to it.
- **Isolation:** agents with `isolation: worktree` work in their own git worktree — see [worktrees.md](../advanced_usage/worktrees.md).
