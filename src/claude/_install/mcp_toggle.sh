#!/bin/bash
set -e

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

ACTION="${1:-}"
shift || true

if [[ -z "${ACTION}" ]]; then
    log_message "${ERROR}" "Usage: mcp_toggle.sh enable|disable <server|group> [...]"
    log_message "${INFO}"  "Groups: dev (github), docs (atlassian), all"
    exit 1
fi

log_message "${DEBUG}" "MCP toggle: ${ACTION} $*"
python3 src/sh/claude/helpers/mcp_toggle.py "${ACTION}" "$@"
