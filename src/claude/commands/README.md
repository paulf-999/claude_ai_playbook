# ⚡ Commands

This page lists all slash commands available during a Claude Code session, describing what each command does and when to use it.

Invoke any command via `/command-name` at the Claude Code prompt.

## 🛠️ Development

| File | Command | Purpose |
|------|---------|---------|
| [`debug.md`](debug.md) | `/debug` | 🐛 Start a structured debugging session using the `debugger` sub-agent |
| [`review.md`](review.md) | `/review` | 🔍 Review current changes using the `code-reviewer` sub-agent |
| [`wrap_up.md`](wrap_up.md) | `/wrap_up` | 🏁 Generate a session summary to paste into `context.md` |

> **Document templates** (design decisions, ideas, platform assessments, requirements) are handled by skills in [`skills/templates/`](../skills/templates/) — they include an interactive elicitation workflow and produce the populated document.
