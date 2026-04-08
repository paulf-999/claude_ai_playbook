# 🖥️ Bash Style Guide & Standards

Defines the team's Bash/Shell scripting standards, structure conventions, and tooling requirements.

## 📄 Template

All new scripts must follow the team bash template:
[`dmt-scripts-git_repo_template/src/templates/bash_script_template.sh`](https://github.com/payroc/dmt-scripts-git_repo_template/blob/main/src/templates/bash_script_template.sh)

---

## 🛡️ Safety flags

All scripts must begin with:

```bash
#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status (fail fast).
```

---

## 🔧 Shell utilities

All scripts must source the shared utilities file at the top:

```bash
source src/sh/shell_utils.sh
```

`shell_utils.sh` provides:

| Utility | Description |
|---|---|
| `log_message "$LEVEL" "$MSG"` | Print a coloured log message |
| `print_section_header "$LEVEL" "$MSG"` | Print a formatted section header |
| `dir_exists "$PATH"` | Returns true if directory exists |
| `file_exists "$PATH"` | Returns true if file exists |
| `handle_interruption` | Signal handler for Ctrl+C — wire up with `trap handle_interruption INT` |

Log level constants (use these as the first argument to logging functions):

| Constant | Colour | Use for |
|---|---|---|
| `${DEBUG}` | Cyan | 🔵 Script start/end, general flow |
| `${DEBUG_DETAILS}` | Purple | 🟣 Lower-level detail |
| `${INFO}` | Green | 🟢 Informational messages |
| `${WARNING}` | Yellow | ⚠️ Non-fatal warnings |
| `${ERROR}` | Red | 🔴 Errors |
| `${CRITICAL}` | Bold red | 🚨 Critical failures |

---

## 🗂️ Script structure

Follow this section order:

```bash
#!/bin/bash
set -e

source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

#=======================================================================
# Functions
#=======================================================================

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Script execution started."

# script logic here

print_section_header "${DEBUG}" "Script execution completed." && echo
```

---

## 🔩 Tooling

- All shell scripts must pass `shellcheck` before committing.
- Resolve all `shellcheck` warnings — suppress only with a documented reason:

```bash
# shellcheck disable=SC2034  # intentionally unused: template placeholder
```

---

## 🏷️ Naming conventions

| Construct | Convention |
|---|---|
| Functions | `snake_case` |
| Variables | `UPPER_SNAKE_CASE` |
| Script files | `snake_case.sh` |

---

## 📦 Variables

- Always quote variable references: `"${VAR}"` not `$VAR`.
- Declare local variables inside functions with `local`.

---

## 🔀 Conditionals

- Use `[[ ]]` over `[ ]` — safer and more expressive.
- Quote all variable references inside conditionals.

---

## 📌 General

- Use absolute paths where the working directory may vary.
- Do not parse `ls` output — use globs or `find` instead.
- Comment non-obvious logic inline; keep comments accurate and up to date.
