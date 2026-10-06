#!/bin/bash
# version: 2.0.1
# created: 2026-08-28
# updated: 2026-10-01
# PreToolUse hook — checks the name of each new file written under the Claude config dir.
# Runs the same file checks as _tests/_file_structure_validator.py on that one path,
# and denies the Write only when the name has an error (e.g. not snake_case), giving the fix.
# Advisory notes are ignored: the "child file" note also fires on correctly named tier rules.
set -e

CLAUDE_HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_ROOT_DIR="$(dirname "${CLAUDE_HOOKS_DIR}")"
CHECKER="${CLAUDE_ROOT_DIR}/_tests/_file_structure_validator.py"

#=======================================================================
# Variables
#=======================================================================

# Read full hook payload from stdin — provided by Claude Code on every tool use.
INPUT=$(cat)

#=======================================================================
# Main script logic
#=======================================================================

# Only intercept Write calls — other tools cannot create new files.
TOOL_NAME=$(echo "${INPUT}" | jq -r '.tool_name // empty' 2>/dev/null)
[[ "${TOOL_NAME}" != "Write" ]] && exit 0

# Only check new files inside the config dir — project files follow their own conventions,
# and existing files already passed the compliance test.
FILE_PATH=$(echo "${INPUT}" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[[ "${FILE_PATH}" != "${CLAUDE_ROOT_DIR}/"* ]] && exit 0
[[ -e "${FILE_PATH}" ]] && exit 0

# Fail open: a missing checker, python3 or a checker error must never block a write.
[[ -f "${CHECKER}" ]] && command -v python3 >/dev/null 2>&1 || exit 0
VIOLATIONS=$(python3 "${CHECKER}" --check "${CLAUDE_ROOT_DIR}" "${FILE_PATH}" 2>/dev/null) || exit 0
ERRORS=$(echo "${VIOLATIONS}" | jq -r '[.[] | select(.severity == "error") | "- " + .message] | join("\n")' 2>/dev/null) || exit 0
[[ -z "${ERRORS}" ]] && exit 0

# Deny the Write and say exactly what to rename.
jq -n \
  --arg file_path "${FILE_PATH}" \
  --arg errors "${ERRORS}" \
  '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":("New config file name breaks the naming standard — rename it and retry.\n\nFile: " + $file_path + "\n" + $errors + "\n\nSee rules/01_essentials/claude_usage_standards/naming_standards.md")}}'
