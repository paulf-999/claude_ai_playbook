#!/bin/bash
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# Description: <one line saying what this script does>
# Usage: src/sh/<script_name>.sh [args] (run from the repo root)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

# Catch Ctrl+C, so an interrupted run says so and exits 1
trap handle_interruption SIGINT

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
print_section_header "${DEBUG}" "Script execution started."

# TODO: add your code here

print_section_header "${DEBUG}" "Script execution completed." && echo
