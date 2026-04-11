#!/bin/bash
set -euo pipefail  # -u: Treat unset variables as an error and exit immediately.
                   # -o pipefail: Return the exit status of the last command in the pipeline that failed.
# Load reusable shell script vars & functions
source src/sh/claude/helpers/claude_file_utils.sh

#=======================================================================
# Functions
#=======================================================================

# User-editable files that must be preserved across updates.
# These are deployed once by make install and owned by the user thereafter.
USER_EDITABLE_FILES=(
    "process/session_input.md"
)

# Remove only repo-managed items from target directory.
# Derived dynamically from SOURCE_DIR so new additions are handled automatically.
# Preserves unmanaged directories (e.g. projects/, plugins/) to avoid data loss.
remove_managed_files() {
    for ITEM in "${SOURCE_DIR}"/*; do
        [[ -e "${ITEM}" ]] || continue
        ITEM_NAME=$(basename "${ITEM}")
        rm -rf "${TARGET_DIR:?}/${ITEM_NAME}"
        log_message "${INFO}" "Removed managed item: ${ITEM_NAME}"
    done
}

# Save user-editable files to a temp location before managed files are removed.
preserve_user_editable_files() {
    for FILE in "${USER_EDITABLE_FILES[@]}"; do
        local TEMP_PATH="/tmp/.claude_preserve_${FILE//\//_}"
        if [[ -f "${TARGET_DIR}/${FILE}" ]]; then
            cp "${TARGET_DIR}/${FILE}" "${TEMP_PATH}"
            log_message "${INFO}" "Preserved user-editable file: ${FILE}"
        fi
    done
}

# Restore user-editable files after managed files have been copied.
restore_user_editable_files() {
    for FILE in "${USER_EDITABLE_FILES[@]}"; do
        local TEMP_PATH="/tmp/.claude_preserve_${FILE//\//_}"
        if [[ -f "${TEMP_PATH}" ]]; then
            cp "${TEMP_PATH}" "${TARGET_DIR}/${FILE}"
            rm "${TEMP_PATH}"
            log_message "${INFO}" "Restored user-editable file: ${FILE}"
        fi
    done
}

# Execute full update flow for Claude files
update_claude_files() {
    validate_source_dir           # from claude_file_utils.sh
    validate_target_dir           # from claude_file_utils.sh
    backup_target_dir "copy"      # from claude_file_utils.sh
    preserve_user_editable_files  # local
    remove_managed_files          # local
    copy_claude_files             # from claude_file_utils.sh
    restore_user_editable_files   # local
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Claude file update started."

update_claude_files
print_operation_summary "update"

print_section_header "${DEBUG}" "Claude file update completed." && echo
