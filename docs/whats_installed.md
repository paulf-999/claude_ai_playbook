# 📦 What's installed

`make install` copies the contents of `src/claude/` into `~/.claude/`. This document describes what each category of file does.

Claude Code loads `CLAUDE.md` on startup — it composes all rules, style guides, and process files via `@import` directives.

---

## 📄 Top-level files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | 🧠 Root config loaded by Claude Code; imports all rules, process, and style files |
| `context.md` | 💾 Carries project context between sessions — Claude produces the summary via `/wrap_up` and the user pastes it in manually |
| `settings.json` | ⚙️ Team baseline Claude Code settings (permissions, MCP servers) |

---

## 🔄 Process

**Location:** [`src/claude/process/`](../src/claude/process/README.md)

Instructions that shape how Claude works within a session: the runtime environment declaration, the planning requirement before non-trivial changes, and the structured session start/end checklist.

---

## 📏 Claude Rules

**Location:** [`src/claude/rules/`](../src/claude/rules/README.md)

Hard constraints that Claude must follow in every session. Covers general behaviour, risky action confirmation, git conventions, file hygiene, security, testing requirements, MCP integration discipline, credit efficiency, and execution transparency.

---

## 🤖 Claude Agents

**Location:** [`src/claude/agents/`](../src/claude/agents/README.md)

Sub-agents are specialised Claude personas selected at the start of each session. Four groups are provided:

- 🎭 **Core** ([`agents/core/`](../src/claude/agents/core/README.md)) — Full-session personas with full tool access (architect, project manager, technical writer).
- 🔧 **Utility** ([`agents/utility/`](../src/claude/agents/utility/README.md)) — Designed for read-only review and diagnostics (code reviewer, debugger).
- ⚙️ **Ops** ([`agents/ops/`](../src/claude/agents/ops/README.md)) — Agents for maintaining and validating the Claude setup itself (new user, claude reviewer).
- 🛠️ **Tools** ([`agents/tools/`](../src/claude/agents/tools/README.md)) — Technology-specific agents, one per style guide. Use for focused work or automated code review on a specific technology.

Pre-populate `~/.claude/process/session_input.md` before launching Claude to select a sub-agent and set a task description without going through interactive prompts. Leave a section commented out to be prompted instead.

---

## ⚡ Claude Commands

**Location:** [`src/claude/commands/`](../src/claude/commands/README.md)

Slash commands available in any Claude Code session:

| Command | Purpose |
|---|---|
| `/debug` | Start a structured debugging session using the `debugger` sub-agent |
| `/review` | Review current changes using the `code_reviewer` sub-agent |
| `/wrap_up` | Generate a session summary to paste into `context.md` |
| `/grill_me` | Stress-test a plan — relentless one-question-at-a-time design interview |
| `/devils_advocate` | Adversarial Author vs Reviewer code review up to N rounds against the current diff |

---

## 🛠️ Claude Skills

**Location:** [`src/claude/skills/`](../src/claude/skills/README.md)

Multi-step reusable workflows invoked via `/skill-name`:

| Skill | Purpose |
|---|---|
| `/commit` | Stage files and create a conventional commit |
| `/create_mr` | Full branch-to-PR workflow |
| `/create_confluence_page` | Interactive dispatcher — create a Confluence page from a pattern (sprint goals, design decision, requirements, incident report, and more) |
| `/draft_comms` | Draft or review a Teams message or email |
| `/schedule_meeting` | Check availability, propose a timeslot, and draft a meeting invite |
| `/snapshot-archiving` | Archive `~/.claude_<timestamp>` snapshot directories into a two-tier age-based structure |
| `/catchup-prep` | Prepare for a 1-to-1 or weekly manager catch-up — gather topics, identify core message, filter async items, prioritise, time-box, and produce a final agenda |
| `/ideas` | Capture and browse ideas via the MCP memory server — tagged with category, priority, and status; persistent across sessions |
| `/todos` | Add, list, and close todos via the MCP memory server — priority-sorted, lifecycle-tracked across sessions |
| `/release` | Create a GitHub Release for a completed phase — checks issues, generates changelog from merged PRs, publishes via `gh` |

---

## 🎨 Style guides

**Location:** [`src/claude/style_guide_standards/`](../src/claude/style_guide_standards/README.md)

Coding standards and platform conventions enforced across all projects:

| Style guide | Coverage |
|---|---|
| Airflow | DAG design, configuration, operators, task dependencies, and best practices |
| Ansible | Playbooks, roles, tasks, secrets, and inventory |
| CI/CD | Azure DevOps and GitHub Actions pipeline standards |
| dbt | Model organisation, naming conventions, YAML properties, snapshots, and macros |
| Docker | Dockerfile structure, layer optimisation, security, and naming |
| Makefile | Target and variable naming, shell variable, and formatting conventions |
| Python | PEP 8 with team overrides, environment setup, dependencies, and pytest standards |
| SQL | Formatting, CTE style, Snowflake data types, and SQLFluff configuration |
| Terraform | Structure, naming, variables, providers, modules, and CI tooling |
| Unix | Bash scripting standards and Oh My Zsh setup |

---

## 🔌 MCP servers

**Setup guide:** [`docs/reference/claude_config/mcp/mcp_setup.md`](reference/claude_config/mcp/mcp_setup.md)

MCP servers extend what Claude can access during a session. Installed separately using dedicated make targets. Core servers are always active; integration servers are disabled by default and enabled per session.

**Core** — `make install_core_mcp_servers`

| Server | Purpose |
|---|---|
| `memory` | 💾 Persistent knowledge graph across sessions |
| `context7` | 📚 Up-to-date library and framework documentation |
| `sequential-thinking` | 🧠 Structured multi-step reasoning |
| `filesystem` | 🗂️ Broader file access beyond the current project (scoped to `$HOME`) |

**Integration** — enabled/disabled per session via `make enable_mcp` / `make disable_mcp`

| Server | Purpose |
|---|---|
| `github` | 🐙 Private GitHub repo access |
| `atlassian` | 🔗 Jira and Confluence access via SSO |
| `o365` | 🪟 Microsoft 365 — Outlook, Teams, SharePoint, Calendar |
| `omni` | 📊 Omni Analytics — natural language queries against governed data models |

---

## 🔌 Plugins

**Reference:** [`docs/reference/claude_config/plugins.md`](reference/claude_config/plugins.md)

**Install:** `make install_plugins`

Claude Code plugins add skills, commands, and hooks directly to the CLI — distinct from MCP servers, which connect Claude to external tools.

| Plugin | Purpose |
|---|---|
| `skill-creator` | Create, iterate on, and evaluate new skills |
| `claude-md-management` | Improve and revise CLAUDE.md files — provides the `/revise-claude-md` command |
| `security-guidance` | Security best-practice guidance during development |
| `pyright-lsp` | Pyright language server — live type checking on Python files (requires `pyright` installed separately) |
| `ralph-loop` | Run a prompt on a recurring loop |

---

## 🪝 Hooks

**Location:** [`src/claude/hooks/`](../src/claude/hooks/)

**Install:** included in `make install`

Hooks are shell or Python scripts wired to Claude Code lifecycle events via `settings.json`. They run automatically — no manual invocation required.

| Hook | Event | Severity model | Purpose |
|---|---|---|---|
| `claude_prompt_reviewer.py` | `UserPromptSubmit` | Low: inject tip into context. High: block prompt. | Checks each prompt against Claude Code best practices — specific file references, verification criteria, and risky/destructive actions. Outputs a tip + candidate improved prompt for low-severity issues; blocks high-severity prompts (e.g. `DROP TABLE`, `rm -rf`, `--force`) until the user revises. |
