#!/bin/bash
# version: 2.0.1
# created: 2026-08-28
# updated: 2026-10-02
# PostToolUse hook — checks where markdown files written inside the Claude config dir live.
# Root: only the known top-level files may sit at the config root (see claude_directory_structure.md).
# Reference: _reference/ files are snake_case topics with no date, or _<aspect>.md children of one topic.
# Every other folder has its own conventions, and files outside the config dir are ignored.
# The edit has already happened, so exit 2 feeds the fix back to Claude rather than blocking.

CLAUDE_HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_ROOT_DIR="$(dirname "${CLAUDE_HOOKS_DIR}")"
STYLE_RULE="rules/01_essentials/claude_usage_standards/writing_style.md"

#=======================================================================
# Variables
#=======================================================================

# Markdown files allowed at the config root
ROOT_FILES=(CLAUDE.md README.md TODO.md aliases.md settings_json_readme.md)

# Claude Code sends the payload as JSON on stdin; a path argument is kept for manual runs.
FILE_PATH="${1:-}"
if [[ -z "${FILE_PATH}" ]]; then
  FILE_PATH=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
fi

#=======================================================================
# Main script logic
#=======================================================================

# Only markdown files inside the config dir are checked.
[[ "${FILE_PATH}" == *.md ]] || exit 0
[[ "${FILE_PATH}" == "${CLAUDE_ROOT_DIR}/"* ]] || exit 0
RELATIVE_PATH="${FILE_PATH#"${CLAUDE_ROOT_DIR}"/}"

if [[ "${RELATIVE_PATH}" != */* ]]; then
  for allowed in "${ROOT_FILES[@]}"; do
    [[ "${RELATIVE_PATH}" == "${allowed}" ]] && exit 0
  done
  PROBLEM="Markdown files don't belong at the config root — move it to _reference/, _docs/ or another folder."
elif [[ "${RELATIVE_PATH}" == _reference/* ]]; then
  [[ "${RELATIVE_PATH}" == */README.md ]] && exit 0
  [[ "${RELATIVE_PATH}" =~ ^_reference/[a-z][a-z0-9_]*\.md$ ]] && exit 0
  [[ "${RELATIVE_PATH}" =~ ^_reference/[a-z][a-z0-9_]*/_[a-z0-9_]+\.md$ ]] && exit 0
  PROBLEM="Reference files are _reference/<topic>.md (snake_case, no date) or _reference/<topic>/_<aspect>.md."
else
  exit 0
fi

cat >&2 << MESSAGE
❌ Markdown file location breaks the writing style conventions:
   Path: ${RELATIVE_PATH}
   ${PROBLEM}

   See: ${STYLE_RULE} → Drafts and errors
MESSAGE
exit 2
