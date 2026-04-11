# 🔌 Claude Code Plugins

Claude Code plugins extend the CLI with additional skills, agents, and hooks. Unlike MCP servers (which connect Claude to external tools and APIs), plugins modify how Claude Code itself behaves — adding workflows, pre-tool hooks, and specialised agents.

Plugins are installed automatically by `make install`. See [`src/sh/claude/install_plugins.sh`](../../../src/sh/claude/install_plugins.sh) for the install script.

---

## 🧪 Evaluating a new plugin

Before adopting a plugin, work through this checklist:

| Question | Notes |
|---|---|
| **What problem does it solve?** | Is this genuinely not covered by existing skills, agents, commands, or MCP servers? |
| **Anthropic official?** | Only install plugins that use hooks if they are from `anthropics/claude-plugins-official` — community plugins with hooks have no oversight and introduce execution risk |
| **Overlap with existing setup?** | Check skills, commands, sub-agents, and MCP servers for duplication before adopting |
| **Token cost** | Always-on plugins (hooks, response modifiers) add tokens on every interaction — factor this in before adopting |
| **Install count and maintenance** | Higher installs and recent activity indicate a healthier plugin |

Only proceed if there is a clear, justified use case not already covered. Log the decision in this file.

---

## ✅ Installed

| Plugin | Commands / behaviour | Hooks | Token cost | Notes |
|---|---|---|---|---|
| [Ralph Loop](https://claude.com/plugins/ralph-loop) | `/ralph-loop <prompt> [--max-iterations N] [--completion-promise TEXT]`, `/cancel-ralph` | Yes — Stop hook intercepts session exit to feed the same prompt back | **High** — each iteration is a full Claude session; always set `--max-iterations` or `--completion-promise` to cap it; without both it runs indefinitely | Installed but not embedded in standard workflows — invoke explicitly for well-defined iterative tasks only |
| [Skill Creator](https://claude.com/plugins/skill-creator) | `/skill-creator` (skill) | No | Moderate — multi-step but bounded; invoked explicitly | Use when creating, evaluating, or improving skills in this repo |
| [CLAUDE.md Management](https://claude.com/plugins/claude-md-management) | `/revise-claude-md` (command), `/claude-md-improver` (skill) | No | Low — reads files and proposes targeted edits | `/revise-claude-md` runs at session wrap-up; `/claude-md-improver` for periodic full audits |
| [Pyright LSP](https://claude.com/plugins/pyright-lsp) | Automatic on `.py`/`.pyi` file edits | No | Low — small consistent overhead per Python file edit | Requires `pip install pyright` (or `pipx install pyright`) to be installed separately |
| [Security Guidance](https://claude.com/plugins/security-guidance) | Automatic — fires before every Edit/Write/MultiEdit | Yes — PreToolUse hook | Low — fires only on file edits | Auto-warns on command injection, XSS, pickle, `eval`, and similar vulnerabilities; no commands to learn |

---

## 🔭 Candidates for evaluation

Ordered by recommended evaluation priority. Score reflects potential usefulness to the DM team (1–10).

| Priority | Plugin | Verified | Installs | Hooks | MCP required | Token cost | Score | What to evaluate |
|---|---|---|---|---|---|---|---|---|
| 1 | [Data](https://claude.com/plugins/data) | ✅ | 1.4k | No | Snowflake / warehouse MCP | Low | **9** | SQL, dataset exploration, visualisations, and dashboards against Snowflake, Databricks, and BigQuery. Requires a database MCP to query live data — without one it falls back to file-based inputs. |
| 2 | [Engineering](https://claude.com/plugins/engineering) | ✅ | N/A | Unknown | GitHub MCP (team has this) | Unknown | **6** | Code review, ADR drafting, incident post-mortems, and standup summaries from commits/PRs. Available in Claude Cowork — verify Claude Code compatibility before adopting. |
| 4 | [PR Review Toolkit](https://claude.com/plugins/pr-review-toolkit) | ✅ | 64k | No | GitHub MCP (team has this) | Moderate | **6** | Six specialised PR review agents (docs accuracy, test coverage, error handling, type design, standards, simplification). Deeper than the existing `code_reviewer` sub-agent. |
| 5 | [Feature Dev](https://claude.com/plugins/feature-dev) | ✅ | 144k | No | — | Moderate | **5** | Structured 7-phase feature workflow with code-explorer, code-architect, and code-reviewer agents. Substantial overlap with the architect sub-agent and `rules/workflows.md`. |
| 6 | [Explanatory Output Style](https://claude.com/plugins/explanatory-output-style) | ✅ | N/A | No | — | **High** — adds explanation boxes to every response | **4** | Adds educational insight boxes to every response. Useful for onboarding; token cost is ongoing — not recommended for regular use. |

### Not recommended

| Plugin | Verified | Reason |
|---|---|---|
| [Code Review](https://claude.com/plugins/code-review) | ✅ | Duplicates existing `code_reviewer` sub-agent and `/review` command |
| [Microsoft Docs](https://claude.com/plugins/microsoft-docs) | ❌ | Not Anthropic verified; only 2.9k installs; low value alongside existing O365 MCP server |
| [Remember](https://claude.com/plugins/remember) | ❌ | Not Anthropic verified; overlaps with the auto-memory system already configured in this playbook |
