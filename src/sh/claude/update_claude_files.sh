#!/bin/bash
set -euo pipefail  # -u: Treat unset variables as an error and exit immediately.
                   # -o pipefail: Return the exit status of the last command in the pipeline that failed.
# Load reusable shell script vars & functions
source src/sh/claude/helpers/claude_file_utils.sh

#=======================================================================
# Functions
#=======================================================================

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

# Execute full update flow for Claude files
update_claude_files() {
    validate_source_dir    # from claude_file_utils.sh
    validate_target_dir    # from claude_file_utils.sh
    backup_target_dir "copy"  # from claude_file_utils.sh
    remove_managed_files   # local
    copy_claude_files      # from claude_file_utils.sh
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Claude file update started."

update_claude_files
print_operation_summary "update"

print_section_header "${DEBUG}" "Claude file update completed." && echo
