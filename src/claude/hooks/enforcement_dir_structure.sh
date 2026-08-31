#!/bin/bash
# PreToolUse hook — enforces directory structure rules for new dirs under ~/.claude/.
# Injects directory structure rules as context before mkdir runs so Claude can confirm
# the proposed directory name and placement follows the standard before proceeding.
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

print_section_header "${DEBUG}" "Enforcement: dir_structure.sh started" >&2 2>/dev/null || true

# Only intercept Bash tool calls — mkdir only runs through Bash.
TOOL_NAME=$(echo "${INPUT}" | jq -r '.tool_name // empty' 2>/dev/null)
[[ "${TOOL_NAME}" != "Bash" ]] && exit 0

# Only act on mkdir commands — other Bash commands are not relevant here.
CMD=$(echo "${INPUT}" | jq -r '.tool_input.command // empty' 2>/dev/null)
[[ "${CMD}" != *"mkdir"* ]] && exit 0

# Only enforce within ~/.claude/ — project directories follow their own conventions.
[[ "${CMD}" != *".claude"* ]] && exit 0

# Load directory structure rules from the appropriate file.
DIR_STRUCTURE_RULES=""

if [[ -f ~/.claude/_rules/01_core/claude_directory_structure/_claude_directory_organization.md ]]; then
  DIR_STRUCTURE_RULES=$(cat ~/.claude/_rules/01_core/claude_directory_structure/_claude_directory_organization.md)
elif [[ -f ~/.claude/_rules/01_core/claude_directory_structure.md ]]; then
  DIR_STRUCTURE_RULES=$(cat ~/.claude/_rules/01_core/claude_directory_structure.md)
else
  DIR_STRUCTURE_RULES="Directory structure rules not found. Check ~/.claude/_rules/01_core/claude_directory_structure.md"
fi

# Inject dir structure rules as context — soft reminder, does not block the mkdir.
jq -n \
  --rawfile rules "$DIR_STRUCTURE_RULES" \
  '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":("Directory structure reminder — confirm this mkdir follows ~/.claude/ conventions:\n\n" + $rules)}}'

print_section_header "${DEBUG}" "Enforcement: dir_structure.sh completed" >&2 2>/dev/null || true
