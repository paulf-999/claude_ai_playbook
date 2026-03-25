#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "Bootstrapping Claude AI playbook structure..."

DIRS=(
  "${ROOT_DIR}/docs"
  "${ROOT_DIR}/src/claude"
  "${ROOT_DIR}/src/claude/commands"
  "${ROOT_DIR}/src/claude/context"
  "${ROOT_DIR}/src/claude/personas"
  "${ROOT_DIR}/src/claude/session"
  "${ROOT_DIR}/src/claude/workflows"
  "${ROOT_DIR}/src/sh/claude"
)

FILES=(
  "${ROOT_DIR}/docs/README.md"
  "${ROOT_DIR}/src/claude/commands/.gitkeep"
  "${ROOT_DIR}/src/claude/context/.gitkeep"
  "${ROOT_DIR}/src/claude/personas/.gitkeep"
  "${ROOT_DIR}/src/claude/session/.gitkeep"
  "${ROOT_DIR}/src/claude/workflows/.gitkeep"
  "${ROOT_DIR}/src/sh/claude/install_claude_files.sh"
  "${ROOT_DIR}/src/sh/claude/update_claude_files.sh"
)

# Create directories
for dir in "${DIRS[@]}"; do
  mkdir -p "${dir}"
done

# Create files (only if missing)
for file in "${FILES[@]}"; do
  if [[ ! -f "${file}" ]]; then
    touch "${file}"
    echo "Created: ${file#${ROOT_DIR}/}"
  else
    echo "Exists:  ${file#${ROOT_DIR}/}"
  fi
done

# Make scripts executable
chmod +x \
  "${ROOT_DIR}/src/sh/claude/bootstrap_claude_repo.sh" \
  "${ROOT_DIR}/src/sh/claude/install_claude_files.sh" \
  "${ROOT_DIR}/src/sh/claude/update_claude_files.sh" || true

echo
echo "✅ Bootstrap complete"
echo
echo "Claude payload structure:"
find "${ROOT_DIR}/src/claude" | sort | sed "s#${ROOT_DIR}/##"
