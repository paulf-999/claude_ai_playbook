#!/bin/bash
# PreToolUse hook — enforces naming conventions for new files under ~/.claude/.
# Blocks the Write tool and injects naming rules so Claude must confirm
# the proposed filename follows the standard before proceeding.
set -e

source ~/.claude/_lib/shell_utils.sh 2>/dev/null || true

#=======================================================================
# Variables
#=======================================================================

# Read full hook payload from stdin — provided by Claude Code on every tool use.
INPUT=$(cat)

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT 2>/dev/null || true

print_section_header "${DEBUG}" "Enforcement: naming_convention.sh started" >&2 2>/dev/null || true

# Only intercept Write calls — other tools cannot create new files.
TOOL_NAME=$(echo "${INPUT}" | jq -r '.tool_name // empty' 2>/dev/null)
[[ "${TOOL_NAME}" != "Write" ]] && exit 0

# Only enforce within ~/.claude/ — project files follow their own conventions.
FILE_PATH=$(echo "${INPUT}" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[[ "${FILE_PATH}" != *".claude/"* ]] && exit 0

# Skip existing files — naming is only a concern at creation time.
[[ -e "${FILE_PATH}" ]] && exit 0

# Load naming conventions from the appropriate rule files.
# Prefer reading the specific child file for focused context.
NAMING_RULES=""

if [[ -f ~/.claude/_rules/01_core/claude_directory_structure/_claude_directory_naming.md ]]; then
  NAMING_RULES=$(cat ~/.claude/_rules/01_core/claude_directory_structure/_claude_directory_naming.md)
elif [[ -f ~/.claude/_rules/01_core/naming_standards/_naming_principles.md ]]; then
  NAMING_RULES=$(cat ~/.claude/_rules/01_core/naming_standards/_naming_principles.md)
else
  # Fallback to parent rules if child files not found
  NAMING_RULES=$(cat ~/.claude/_rules/01_core/naming_standards.md 2>/dev/null || echo "Naming standards rule file not found. Check ~/.claude/_rules/01_core/naming_standards.md")
fi

# Block and surface the naming conventions so Claude reviews the proposed name.
jq -n \
  --rawfile conventions "$NAMING_RULES" \
  '{"decision":"block","reason":("New file detected under ~/.claude/. Review naming conventions before proceeding.\n\nFile: " + $ENV.FILE_PATH + "\n\n" + $conventions)}'

print_section_header "${DEBUG}" "Enforcement: naming_convention.sh completed" >&2 2>/dev/null || true
