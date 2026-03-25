#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status (fail fast).

# Load reusable shell script vars & functions
source src/sh/claude/claude_file_utils.sh

#=======================================================================
# Functions
#=======================================================================

# Execute full install flow for Claude files
install_claude_files() {
    validate_source_dir          # from claude_file_utils.sh
    create_target_dir_if_missing # from claude_file_utils.sh
    backup_target_dir "move"     # from claude_file_utils.sh
    copy_claude_files            # from claude_file_utils.sh
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Claude file installation started."

install_claude_files
print_operation_summary "installation"

print_section_header "${DEBUG}" "Claude file installation completed." && echo
