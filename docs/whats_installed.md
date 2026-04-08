# 📦 What's installed

`make install` copies the contents of `src/claude/` into `~/.claude/`. This document describes what each category of file does.

---

## 📏 Claude Rules

**Location:** [`src/claude/rules/`](../src/claude/rules/README.md)

Hard constraints that Claude must follow in every session. Covers general behaviour, risky action confirmation, git conventions, file hygiene, security, and testing requirements.

---

## 🔄 Process

**Location:** [`src/claude/process/`](../src/claude/process/README.md)

Instructions that shape how Claude works within a session: the runtime environment declaration, the planning requirement before non-trivial changes, and the structured session start/end checklist.

---

## 🤖 Claude Agents

**Location:** [`src/claude/agents/`](../src/claude/agents/README.md)

Sub-agents are specialised Claude personas selected at the start of each session. Two groups are provided:

- 🔧 **Core** ([`agents/core/`](../src/claude/agents/core/README.md)) — General-purpose agents covering code review, debugging, devops, and technical writing.
- 🏢 **DMT** ([`agents/dmt/`](../src/claude/agents/dmt/README.md)) — Team-specific agents for data analytics, data engineering, platform architecture, and project management.

---

## ⚡ Claude Commands

**Location:** [`src/claude/commands/`](../src/claude/commands/README.md)

Slash commands available in any Claude Code session. Includes `/adr`, `/debug`, `/review`, and `/wrap_up`.

---

## 🛠️ Claude Skills

**Location:** [`src/claude/skills/`](../src/claude/skills/README.md)

Multi-step reusable workflows. Currently includes `commit` (conventional commit workflow) and `create-mr` (full branch-to-PR workflow).

---

## 🎨 Style guides

**Location:** [`src/claude/style_guide_standards/`](../src/claude/style_guide_standards/README.md)

Language-specific coding standards for Bash, Python, and SQL.

---

## 🔌 MCP servers

**Setup guide:** [`docs/reference/mcp/mcp_setup.md`](reference/mcp/mcp_setup.md)

MCP servers extend what Claude can access during a session. They are installed separately from `make install` using dedicated make targets. Includes key integrations (GitHub, Atlassian, Microsoft 365) and core tooling servers (memory, context7, sequential-thinking, filesystem).

---

## 📄 Top-level files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | 🧠 Root config loaded by Claude Code; imports all rules, process, and style files |
| `context.md` | 💾 Carries project context between sessions — Claude produces the summary via `/wrap_up` and the user pastes it in manually |
| `settings.json` | ⚙️ Team baseline Claude Code settings (permissions, MCP servers, hooks) |
