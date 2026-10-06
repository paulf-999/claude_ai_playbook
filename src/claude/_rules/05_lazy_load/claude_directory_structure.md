---
paths:
  - "**/.claude/**"
  - "**/claude/**"
---
<!-- version: 1.3.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
<!-- miss_cost: low — a badly named or misplaced config file, which the naming-convention hook also blocks -->
<!-- loading: path-scoped — loads with config-directory files through paths:, and through a pointer in claude_usage_standards.md for a new file -->
# 🗂️ Directory Structure — `~/.claude/`

**Purpose:** Establish conventions for how the Claude config directory is organized, distinguishing user-created from auto-generated directories, and ensure files are placed in their appropriate locations.

Applies to all file and directory creation in `~/.claude/` and the playbook repo's `src/claude/`.

## 📋 Contents

- [Directory organization](#-directory-organization) — what directories exist and their purpose
- [Naming conventions](#-naming-conventions) — how directories and files should be named
- [Validation](#-validation) — how to validate file structure compliance

---

## 🏗️ Directory organization

- **Read on demand:** `~/.claude/_rules/05_lazy_load/claude_directory_structure/_claude_directory_organisation.md` — loads with the same files through paths:

## 🏷️ Naming conventions

- **Read on demand:** `~/.claude/_rules/05_lazy_load/claude_directory_structure/_claude_directory_naming.md` — loads with the same files through paths:

## ✅ Validation

- **Read on demand:** `~/.claude/_rules/05_lazy_load/claude_directory_structure/_file_structure_validation.md` — loads with the same files through paths:

---

## 📖 Reference (architectural overview)

- **Read on demand:** `~/.claude/_reference/claude_config_architecture.md` — architectural overview, design principles and the rationale for the directory layout
