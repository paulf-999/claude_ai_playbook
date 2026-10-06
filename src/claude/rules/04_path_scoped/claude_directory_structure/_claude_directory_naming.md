---
paths:
  - "**/.claude/**"
  - "**/claude/**"
---
<!-- version: 3.1.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
# 🏷️ Naming — Directories and Files

**Purpose:** Set the prefix conventions that tell user-created directories, auto-generated directories and child files apart in the Claude config.

- **General naming rules:** snake_case, self-describing names, naming for scale and offering options live in `naming_standards/_naming_principles.md`.
- **Hook, skill and rule patterns:** live in `naming_standards/_claude_naming_patterns.md`.

---

## 🏗️ Directory and file prefixes

| Type | Pattern | Example | Note |
|---|---|---|---|
| **User-created** | `_<name>/` | `_rules_lazy_load/`, `_templates/`, `_docs/` | Always underscore prefix |
| **Auto-generated** | `<name>/` | `backups/`, `memory/`, `sessions/` | Never touch these |
| **Child file** | `_<aspect>.md` | `_claude_directory_organisation.md` | Prefix indicates child of parent |

- **User-created directories:** must start with an underscore — `_rules_lazy_load/`, `_templates/`, `_reference/`.
- **Auto-generated directories:** have no prefix — `backups/`, `memory/`, `sessions/`.
- **Child files:** start with an underscore to distinguish them from top-level files — `_child_file.md`.
