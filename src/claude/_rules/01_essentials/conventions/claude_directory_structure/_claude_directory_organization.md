# 🏗️ Directory Organization — `~/.claude/`

**Purpose:** Define what directories exist in the Claude config, their purpose, and the distinction between user-created and auto-generated directories.

---

## 📁 Directory types

- **User-created dirs:** underscore prefix — e.g. `_docs/`, `_rules/`, `_templates/`, `_reference/`, `_tests/`
  - **Pattern:** `_<name>/` — user explicitly creates these to organize content
  - **Note:** These directories are tracked in version control and intentionally maintained
- **Claude Code auto-generated dirs:** no prefix — e.g. `backups/`, `memory/`, `sessions/`, `projects/`
  - **Pattern:** `<name>/` — Claude Code creates these automatically; you should not manually create them
  - **Note:** These are excluded from version control (`.gitignore`)

---

## 📂 Directory Tiers

`~/.claude/` is organized into four tiers by purpose and audience:

**Tier 1: Top-level config files**
- `CLAUDE.md`, `aliases.md`, `settings.json`, `keybindings.json` — entry points and user-facing configuration

**Tier 2: Core rules (_rules/)**
- `01_essentials/` — blocking/safety rules (always-on imports; user-facing guidance)
- `02_claude_standards/` — quality gates and operational standards (always-on imports)
- `03_claude_reference/` — system knowledge and reference docs (always-on imports)
- `04_lazy_load/` — domain-specific rules (loaded on-demand; token-efficient)

**Tier 3: Infrastructure (_tests/, _templates/, _reference/, _docs/)**
- Tests, templates, evergreen reference docs, and additional documentation

**Tier 4: Domain-specific (agents/, hooks/, skills/, wip/)**
- Custom sub-agents, enforcement/style-guide hooks, reusable skills, work-in-progress features

**Tier 5: Auto-generated (backups/, memory/, projects/, sessions/)**
- Claude Code-managed; excluded from version control; never manually edited

**Authoritative source:** For the current, always-up-to-date directory listing, consult the README.md in each tier (e.g., `_rules/README.md`, `agents/README.md`, `hooks/README.md`). These are maintained by humans and tools; this document describes the organizational *principle*, not a comprehensive inventory.

---

## 🔀 When to create a subdirectory

Create a subdirectory when **two or more related files** share the same theme and benefit from grouping:

- ✅ Create when: `naming_standards/` contains `_naming_principles.md` + `_claude_naming_patterns.md` (related, reusable grouping)
- ✅ Create when: `claude_directory_structure/` contains `_claude_directory_organization.md` + `_claude_directory_naming.md` (organization + naming are paired concerns)
- ❌ Avoid when: one file stands alone (e.g. a single style guide doesn't need a folder)

**Note:** Prefer flat `_rules/*.md` for standalone rules; introduce a subdir only when the grouping is clear and reusable.

---

## ✅ Rules

- **User-created directories always have underscore prefix** — `_rules/`, `_tests/`, `_templates/`, `_reference/`, `_docs/`
- **Auto-generated directories have no prefix** — `backups/`, `memory/`, `sessions/`, `projects/`
- **When unsure if a directory is auto-generated:** Check `~/.claude/.gitignore` — auto-generated dirs are typically excluded
- **Never create files directly in `~/.claude/` root** — they belong in `_docs/`, `_reference/`, or a domain-specific subdirectory

---

## 🔗 Related rules

- **Parent:** `claude_directory_structure.md` — entry point; organization and naming overview
- **Sibling:** `_claude_directory_naming.md` — naming patterns for files and directories
- **Related:** `writing_style.md` → `_multifile_document_organization.md` — when to split documents into parent + child files
- **Related:** `authoring_rules.md` — directory placement for new rules (01_essentials, 02_claude_internal, 03_lazy_load)
