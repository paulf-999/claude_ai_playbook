#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status (fail fast).

# Load reusable shell script vars & functions
source src/sh/claude/claude_file_utils.sh

#=======================================================================
# Functions
#=======================================================================

# Remove and recreate target directory for clean update
refresh_target_dir() {
    rm -rf "${TARGET_DIR}"
    mkdir -p "${TARGET_DIR}"
    log_message "${INFO}" "Refreshed target directory: ${TARGET_DIR}"
}

# Execute full update flow for Claude files
update_claude_files() {
    validate_source_dir  # from claude_file_utils.sh
    validate_target_dir  # from claude_file_utils.sh
    backup_target_dir "copy"  # from claude_file_utils.sh
    refresh_target_dir   # local
    copy_claude_files    # from claude_file_utils.sh
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Claude file update started."

update_claude_files
print_operation_summary "update"

print_section_header "${DEBUG}" "Claude file update completed." && echo
