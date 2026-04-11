# ⚡ Commands

This page lists all slash commands available during a Claude Code session, describing what each command does and when to use it.

Invoke any command via `/command-name` at the Claude Code prompt.

## 🛠️ Development

| File | Command | Purpose |
|------|---------|---------|
| [`debug.md`](debug.md) | `/debug` | 🐛 Start a structured debugging session using the `debugger` sub-agent |
| [`review.md`](review.md) | `/review` | 🔍 Review current changes using the `code_reviewer` sub-agent |
| [`wrap_up.md`](wrap_up.md) | `/wrap_up` | 🏁 Generate a session summary to paste into `context.md` |
| [`grill_me.md`](grill_me.md) | `/grill_me` | 🔥 Stress-test a plan or design — Claude interviews you relentlessly, resolving the decision tree one question at a time |
| [`devils_advocate.md`](devils_advocate.md) | `/devils_advocate` | 😈 Adversarial code review — simulates an Author vs Reviewer debate across up to N rounds, covering correctness, security, maintainability, and test gaps |

> **Document templates** (design decisions, ideas, platform assessments, requirements) are handled by the [`/create_confluence_page`](../skills/create_confluence_page/) skill — it includes an interactive elicitation workflow and produces the populated document.
