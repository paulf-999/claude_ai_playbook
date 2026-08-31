#!/bin/bash

#=======================================================================
# Variables
#=======================================================================

# ANSI colour constants — exported so sourcing scripts can reference them directly.
export DEBUG='\033[0;36m'          # cyan — script start/end, general flow
export DEBUG_DETAILS='\033[0;35m'  # purple — lower-level detail
export INFO='\033[0;32m'           # green — informational messages
export WARNING='\033[0;33m'        # yellow — non-fatal warnings
export ERROR='\033[0;31m'          # red — errors
export CRITICAL='\033[1;31m'       # bold red — critical failures
export COLOUR_OFF='\033[0m'

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

#=======================================================================
# Functions
#=======================================================================

log_message() {
    local LOGGING_LEVEL="$1"
    local MESSAGE="$2"
    echo && echo -e "${LOGGING_LEVEL}${MESSAGE}${COLOUR_OFF}"
}

print_section_header() {
    local LOG_LEVEL="$1"
    local MESSAGE="$2"
    echo && echo -e "${LOG_LEVEL}#--------------------------------------------------------------------------------------------"
    echo -e "${LOG_LEVEL}# ${MESSAGE}${COLOUR_OFF}"
    echo -e "${LOG_LEVEL}#--------------------------------------------------------------------------------------------${COLOUR_OFF}"
}

dir_exists() {
    [ -d "$1" ]
}

file_exists() {
    [ -f "$1" ]
}

handle_interruption() {
    log_message "${WARNING}" "Script execution aborted by the user."
    exit 1
}
