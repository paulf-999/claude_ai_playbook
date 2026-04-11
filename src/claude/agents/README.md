# 🤖 Agents

Sub-agents are specialised Claude personas. Each runs in its own context window with a focused system prompt, specific tool access, and independent permissions.

Four directories, each with a distinct purpose:

| Directory | Purpose |
|-----------|---------|
| 🎭 [`core/`](core/README.md) | Full-session personas with full tool access — use for open-ended sessions |
| 🔧 [`utility/`](utility/README.md) | Read-only review and diagnostic agents |
| ⚙️ [`ops/`](ops/README.md) | Agents for maintaining and validating the Claude setup itself |
| 🛠️ [`tools/`](tools/README.md) | Technology-specific agents — one per style guide; use for focused work or automated code review |
