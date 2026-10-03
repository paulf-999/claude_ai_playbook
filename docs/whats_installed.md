# 📦 What's installed

Last updated: 3rd October 2026

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

## 🧰 Templates and reference

See [`src/claude/_templates/README.md`](../src/claude/_templates/README.md) · [`src/claude/_reference/README.md`](../src/claude/_reference/README.md)

Starting templates for new artefacts, and architecture docs that are read on demand.
