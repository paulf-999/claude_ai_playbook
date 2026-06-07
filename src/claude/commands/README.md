# ⚡ Commands

Slash commands available during a Claude Code session. Invoke via `/command-name` at the prompt.

## 🛠️ Development

| File | Command | Purpose | Tested | Status |
|------|---------|---------|--------|--------|
| [`debug.md`](debug.md) | `/debug` | 🐛 Start a structured debugging session using the `debugger` sub-agent | no | active |
| [`review.md`](review.md) | `/review` | 🔍 Review current changes using the `code_reviewer` sub-agent | no | active |
| [`wrap_up.md`](wrap_up.md) | `/wrap_up` | 🏁 Generate a session summary to paste into `context.md` | no | active |
| [`grill_me.md`](grill_me.md) | `/grill_me` | 🔥 Stress-test a plan or design — Claude interviews you relentlessly, resolving the decision tree one question at a time | no | active |
| [`devils_advocate.md`](devils_advocate.md) | `/devils_advocate` | 😈 Adversarial code review — simulates an Author vs Reviewer debate across up to N rounds, covering correctness, security, maintainability, and test gaps | no | active |

> **Document templates** (design decisions, ideas, platform assessments, requirements) are handled by the [`/confluence_create_page`](../skills/confluence_create_page/) skill — it includes an interactive elicitation workflow and produces the populated document.
