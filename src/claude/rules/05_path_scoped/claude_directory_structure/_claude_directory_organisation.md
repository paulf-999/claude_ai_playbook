---
paths:
  - "**/.claude/**"
  - "**/claude/**"
---
<!-- version: 2.0.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
# 🏗️ Directory Organisation — `~/.claude/`

**Purpose:** Define what directories exist in the Claude config, their purpose, and the distinction between user-created and auto-generated directories.

---

## 📁 Directory types

- **User-created dirs:** underscore prefix — e.g. `_docs/`, `_rules_lazy_load/`, `_templates/`, `_reference/`, `_tests/`
  - **Pattern:** `_<name>/` — user explicitly creates these to organise content
  - **Note:** These directories are tracked in version control and intentionally maintained
- **Claude Code auto-generated dirs:** no prefix — e.g. `backups/`, `memory/`, `sessions/`, `projects/`
  - **Pattern:** `<name>/` — Claude Code creates these automatically; you should not manually create them
  - **Note:** These are excluded from version control (`.gitignore`)

---

## 📂 Directory Tiers

`~/.claude/` is organised into five tiers by purpose and audience:

**Tier 1: Top-level config files**
- `CLAUDE.md`, `aliases.md`, `settings.json`, `keybindings.json` — entry points and user-facing configuration

**Tier 2: Core rules (rules/, _rules_lazy_load/)**
- `rules/`: tiers `01_essentials/` to `04_claude_reference/` load every session, and `05_path_scoped/` loads with matching files — Claude Code reads this folder natively, so it has no underscore
- `_rules_lazy_load/`: rules read on demand, plus the tier READMEs — see `claude_rule_loading_strategy.md` for what belongs where

**Tier 3: Infrastructure (_tests/, _templates/, _reference/, _docs/)**
- Tests, templates, evergreen reference docs, and additional documentation

**Tier 4: Domain-specific (agents/, hooks/, skills/, wip/)**
- Custom sub-agents, enforcement/style-guide hooks, reusable skills, work-in-progress features

**Tier 5: Auto-generated (backups/, memory/, projects/, sessions/)**
- Claude Code-managed; excluded from version control; never manually edited

**Authoritative source:** For the current, always-up-to-date directory listing, consult the README.md in each tier (e.g., `_rules_lazy_load/_tier_readmes/00_rules_overview.md`, `agents/README.md`, `hooks/README.md`). These are maintained by humans and tools; this document describes the organisational *principle*, not a comprehensive inventory.

---

## 🔀 When to create a subdirectory

Create a subdirectory when **two or more related files** share the same theme and benefit from grouping:

- ✅ Create when: `naming_standards/` contains `_naming_principles.md` + `_claude_naming_patterns.md` (related, reusable grouping)
- ✅ Create when: `claude_directory_structure/` contains `_claude_directory_organisation.md` + `_claude_directory_naming.md` (organisation + naming are paired concerns)
- ❌ Avoid when: one file stands alone (e.g. a single style guide doesn't need a folder)

**Note:** Prefer a flat `<tier>/<rule>.md` for standalone rules; introduce a subdir only when the grouping is clear and reusable.

---

## ✅ Rules

- **User-created directories always have underscore prefix** — `_rules_lazy_load/`, `_tests/`, `_templates/`, `_reference/`, `_docs/`
- **Auto-generated directories have no prefix** — `backups/`, `memory/`, `sessions/`, `projects/`
- **When unsure if a directory is auto-generated:** Check `~/.claude/.gitignore` — auto-generated dirs are typically excluded
- **Never create files directly in `~/.claude/` root** — they belong in `_docs/`, `_reference/`, or a domain-specific subdirectory
