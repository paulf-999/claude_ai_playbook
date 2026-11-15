---
paths:
  - "**/Makefile"
  - "**/*.mk"
---
<!-- version: 1.2.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-11-15 -->
<!-- miss_cost: low — Makefile style drift -->
<!-- loading: path-scoped — only applies to Makefiles, so it loads when a Makefile is open -->
# 🛠️ Makefile Style Guide & Standards

**Purpose:** Define the team's standards for writing and structuring Makefiles.

## 📋 Structure

- [**Naming Conventions**](makefile/_naming_conventions.md) — Target and variable naming standards
- [**Variables, Operators & Commands**](makefile/_variables_operators_and_commands.md) — SHELL, `:=` operator, display functions, command silencing, automatic variables

## ⚠️ Accepted exceptions

A Makefile may break three of these rules on purpose:

- **Coloured `@echo`:** status lines use `@echo` with colour codes, so each line prints in order with the recipe's shell steps.
- **Uppercase colour constants:** shared terminal codes such as `INFO` and `COLOUR_OFF` stay uppercase to stand apart from settings.
- **`SHELL = <path>`:** setting the shell with `=` behaves the same as `:=` for a fixed value.
