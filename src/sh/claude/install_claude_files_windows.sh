#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status (fail fast).

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh
source src/sh/claude/helpers/claude_file_utils.sh  # sets SOURCE_DIR, TARGET_DIR, BACKUP_DIR

#=======================================================================
# Functions
#=======================================================================

# Resolve the Windows username from the Windows environment via powershell.exe.
# Returns non-zero if detection fails (not in WSL or powershell.exe unavailable).
detect_windows_user() {
    if ! command -v powershell.exe &>/dev/null; then
        log_message "${ERROR}" "powershell.exe not found. This script must be run from WSL2."
        return 1
    fi
    local WIN_USER
    WIN_USER=$(powershell.exe -Command "echo \$env:USERNAME" 2>/dev/null | tr -d '\r\n')
    if [[ -z "${WIN_USER}" ]]; then
        log_message "${ERROR}" "Could not detect Windows username."
        return 1
    fi
    echo "${WIN_USER}"
}

# Override the TARGET_DIR and BACKUP_DIR variables (set by claude_file_utils.sh)
# to point at the Windows user's .claude directory via the WSL2 /mnt/c mount.
set_windows_target_dirs() {
    local WIN_USER="$1"
    TARGET_DIR="/mnt/c/Users/${WIN_USER}/.claude"
    BACKUP_DIR="/mnt/c/Users/${WIN_USER}/.claude_backup_${TIMESTAMP}"
    log_message "${DEBUG}" "Windows target directory: ${TARGET_DIR}"
}

# User-editable files that must be preserved across updates.
# Mirrors the list in update_claude_files.sh.
USER_EDITABLE_FILES=(
    "process/session_input.md"
)

# Save user-editable files to a temp location before managed files are removed.
preserve_user_editable_files() {
    for FILE in "${USER_EDITABLE_FILES[@]}"; do
        local TEMP_PATH="/tmp/.claude_win_preserve_${FILE//\//_}"
        if [[ -f "${TARGET_DIR}/${FILE}" ]]; then
            cp "${TARGET_DIR}/${FILE}" "${TEMP_PATH}"
            log_message "${INFO}" "Preserved user-editable file: ${FILE}"
        fi
    done
}

# Restore user-editable files after managed files have been copied.
restore_user_editable_files() {
    for FILE in "${USER_EDITABLE_FILES[@]}"; do
        local TEMP_PATH="/tmp/.claude_win_preserve_${FILE//\//_}"
        if [[ -f "${TEMP_PATH}" ]]; then
            cp "${TEMP_PATH}" "${TARGET_DIR}/${FILE}"
            rm "${TEMP_PATH}"
            log_message "${INFO}" "Restored user-editable file: ${FILE}"
        fi
    done
}

# Remove only repo-managed items from the Windows .claude directory.
# Preserves unmanaged items (sessions/, plugins/, settings.json, etc.)
# to avoid destroying Windows-specific app state.
remove_managed_files() {
    for ITEM in "${SOURCE_DIR}"/*; do
        [[ -e "${ITEM}" ]] || continue
        local ITEM_NAME
        ITEM_NAME=$(basename "${ITEM}")
        if [[ -e "${TARGET_DIR}/${ITEM_NAME}" ]]; then
            rm -rf "${TARGET_DIR:?}/${ITEM_NAME}"
            log_message "${INFO}" "Removed managed item: ${ITEM_NAME}"
        fi
    done
}

# Execute the full Windows sync flow.
# Always uses update semantics (copy backup, not move) to preserve
# Windows-specific .claude state (sessions, settings.json, plugins, etc.).
sync_windows_claude_files() {
    local WIN_USER
    WIN_USER=$(detect_windows_user)

    set_windows_target_dirs "${WIN_USER}"
    validate_source_dir               # from claude_file_utils.sh
    create_target_dir_if_missing      # from claude_file_utils.sh
    backup_target_dir "copy"          # from claude_file_utils.sh
    preserve_user_editable_files
    remove_managed_files
    copy_claude_files                 # from claude_file_utils.sh
    flatten_skills                    # from claude_file_utils.sh
    restore_user_editable_files
}

# Print a reminder if the Claude CLI is not yet installed on Windows.
check_windows_claude_cli() {
    local CLAUDE_WIN_PATH="/mnt/c/Users/$(detect_windows_user)/AppData/Roaming/npm/claude"
    if [[ ! -f "${CLAUDE_WIN_PATH}" ]]; then
        log_message "${WARNING}" "Claude CLI not detected on Windows."
        log_message "${WARNING}" "To install it, run from a Windows terminal (PowerShell/CMD):"
        log_message "${WARNING}" "  winget install OpenJS.NodeJS.LTS"
        log_message "${WARNING}" "  (open a new terminal, then)"
        log_message "${WARNING}" "  npm install -g @anthropic-ai/claude-code"
    fi
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Windows Claude file sync started."

sync_windows_claude_files
print_operation_summary "Windows sync"
check_windows_claude_cli

print_section_header "${DEBUG}" "Windows Claude file sync completed." && echo
