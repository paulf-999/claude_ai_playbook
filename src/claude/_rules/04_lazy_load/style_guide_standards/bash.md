# 🖥️ Bash Style Guide

**Purpose:** Establish shell scripting conventions for safety, consistency, and maintainability across all Bash scripts in the team.

## 📋 Contents

- [📄 Script structure](#-script-structure)
- [🛡️ Safety flags](#-safety-flags)
- [🔧 Shell utilities](#-shell-utilities)
- [🔩 Tooling](#-tooling)
- [🏷️ Naming conventions](#-naming-conventions)
- [📦 Variables](#-variables)
- [🔀 Conditionals](#-conditionals)
- [📌 General](#-general)

---
## 📄 Script structure

All new scripts must start from the canonical template for correct section order (shebang, safety flags, shell_utils source, section headers, trap, logging):

- **Template location:** `~/.claude/_rules/04_lazy_load/style_guide_standards/unix/templates/template_bash_script.sh`
- **Always reference:** read the template before writing a new script

## 🛡️ Safety flags

All scripts must begin with:

```bash
#!/bin/bash
set -e
```

## 🔧 Shell utilities

All scripts must source the shared utilities file at the top:

```bash
source src/sh/shell_utils.sh
```

- **Canonical source:** `~/.claude/_lib/shell_utils.sh` — copy into `src/sh/` for each project
- **Provides:** `log_message`, `print_section_header`, `dir_exists`, `file_exists`, `handle_interruption`
- **Log levels:** use the correct constant for the severity:
  - `${DEBUG}` (cyan) — script start/end, general flow
  - `${DEBUG_DETAILS}` (purple) — lower-level detail
  - `${INFO}` (green) — informational messages
  - `${WARNING}` (yellow) — non-fatal warnings
  - `${ERROR}` (red) — errors
  - `${CRITICAL}` (bold red) — critical failures

## 🔩 Tooling

- **Linting:** all scripts must pass `shellcheck` before committing
- **Suppression:** only suppress warnings with a documented reason:

```bash
# shellcheck disable=SC2034  # intentionally unused: template placeholder
```

## 🏷️ Naming conventions

- **Functions:** `snake_case`
- **Variables:** `UPPER_SNAKE_CASE`
- **Script files:** `snake_case.sh`

## 📦 Variables

- **Quote all references:** use `"${VAR}"` not `$VAR`
- **Function scope:** declare local variables with `local`

## 🔀 Conditionals

- **Prefer `[[ ]]`** over `[ ]` — safer and more expressive
- **Quote variables:** inside all conditionals

## 📌 General

- **Absolute paths:** use them where the working directory may vary
- **Avoid `ls` parsing:** use globs or `find` instead
- **Comments:** place above the code they describe, not at the end — keep them accurate and up to date
