# 📦 What's installed

Last updated: 1st October 2026

This page gives a one-line overview of each part of `src/claude/`, and links to where the detail lives.

- **Install:** `make install` copies `src/claude/` into `CLAUDE_CONFIG_DIR`, or Claude Code's default `~/.claude` when it isn't set.
- **Loading:** Claude Code reads `CLAUDE.md` at startup, which `@import`s the always-on rules.

---

## 📄 Top-level files

See [`src/claude/README.md`](../src/claude/README.md)

The root config, settings and aliases that every session starts from.

---

## 📏 Rules

See [`src/claude/_rules/README.md`](../src/claude/_rules/README.md)

Five numbered tiers of rules: tiers 01–04 load every session, and `05_lazy_load/` is read on demand.

### 🎯 Path-scoped rules

See [`src/claude/_rules/05_lazy_load/`](../src/claude/_rules/05_lazy_load/)

Lazy-load rules with `paths:` frontmatter, which Claude Code loads automatically when Claude reads a matching file, such as `sql.md` for `.sql` files. `make install` links them into the `rules/` folder of your config, the only place Claude Code looks for them.

---

## 🎨 Style guides

See [`src/claude/_rules/05_lazy_load/style_guide_standards/`](../src/claude/_rules/05_lazy_load/style_guide_standards/)

Coding standards for the technologies the team uses, read on demand unless a path-scoped rule loads them.

---

## 🤖 Agents

See [`src/claude/agents/`](../src/claude/agents/)

Specialised sub-agents Claude can hand a task to, grouped by domain folder.

---

## 🛠️ Skills

See [`src/claude/skills/README.md`](../src/claude/skills/README.md)

Multi-step workflows invoked with `/<skill_name>`, grouped by domain folder.

---

## 🪝 Hooks

See [`src/claude/hooks/`](../src/claude/hooks/)

Shell scripts that run at Claude Code lifecycle events once registered in `settings.json`.

---

## 🐍 Scripts

See [`src/claude/_scripts/`](../src/claude/_scripts/)

Python tools for auditing the config, such as `make audit_components`, which reports on the health of skills, agents and rules, and `make audit_rule_usage`, which measures how often each rule applies and loads.

---

## 🧰 Templates and reference

See [`src/claude/_templates/README.md`](../src/claude/_templates/README.md) · [`src/claude/_reference/README.md`](../src/claude/_reference/README.md)

Starting templates for new artefacts, and architecture docs that are read on demand.

---

## 🔌 MCP servers

See [`docs/reference/claude_config/mcp/mcp_setup.md`](reference/claude_config/mcp/mcp_setup.md)

Connections to external tools, such as Atlassian, toggled with `make enable_mcp` and `make disable_mcp`.

---

## 🧩 Plugins

See [`docs/reference/claude_config/plugins.md`](reference/claude_config/plugins.md)

Add-ons that bring extra skills, commands and hooks to the CLI, installed with `make install_plugins`.
