#!/bin/bash
set -e

source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

# TODO: declare variables here

#=======================================================================
# Functions
#=======================================================================

# TODO: add functions here

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Script execution started."

# TODO: add your code here

print_section_header "${DEBUG}" "Script execution completed." && echo
