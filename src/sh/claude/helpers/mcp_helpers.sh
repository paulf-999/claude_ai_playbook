#!/bin/bash

# Shared helper functions for MCP server installation

# Return 0 if a server name is already registered, 1 otherwise
is_installed() {
    local SERVER_NAME="$1"
    claude mcp list 2>/dev/null | grep -q "^${SERVER_NAME}"  # match server name at start of line
}

# Verify a server is registered after installation
verify_installation() {
    local NAME="$1"
    log_message "${DEBUG}" "Verifying '${NAME}' MCP server registration..."
    if claude mcp list 2>/dev/null | grep -q "^${NAME}"; then
        log_message "${INFO}" "Verification passed — '${NAME}' is registered."
    else
        log_message "${WARNING}" "Verification failed — '${NAME}' not found in mcp list."
    fi
}

# Install a single npx-based MCP server
install_npx_server() {
    local NAME="$1"
    local COMMAND="$2"

    if is_installed "${NAME}"; then
        log_message "${INFO}" "Skipping '${NAME}' — already registered."
    else
        log_message "${DEBUG}" "Installing '${NAME}'..."
        claude mcp add --scope user "${NAME}" -- ${COMMAND}  # -- separates claude args from the npx command
        log_message "${INFO}" "Installed '${NAME}'."
        verify_installation "${NAME}"
    fi
}

# Install the filesystem MCP server, scoped to the user's home directory
install_filesystem_server() {
    if is_installed "filesystem"; then
        log_message "${INFO}" "Skipping 'filesystem' — already registered."
    else
        log_message "${DEBUG}" "Installing 'filesystem' (scoped to ${HOME})..."
        claude mcp add --scope user filesystem -- npx -y @modelcontextprotocol/server-filesystem "${HOME}"  # scoped to $HOME for broad but bounded access
        log_message "${INFO}" "Installed 'filesystem'."
        verify_installation "filesystem"
    fi
}

# Print a reminder about the Microsoft 365 connector (cannot be scripted)
print_o365_reminder() {
    echo
    log_message "${WARNING}" "#--------------------------------------------------------------------------------------------"
    log_message "${WARNING}" "# Manual step required: Microsoft 365 connector"
    log_message "${WARNING}" "#--------------------------------------------------------------------------------------------"
    log_message "${WARNING}" "# The Microsoft 365 connector is a Claude web UI integration and cannot be configured"
    log_message "${WARNING}" "# via the CLI. To enable it:"
    log_message "${WARNING}" "#"
    log_message "${WARNING}" "#   1. Open Claude at https://claude.ai"
    log_message "${WARNING}" "#   2. Go to Settings > Connectors"
    log_message "${WARNING}" "#   3. Find and enable the Microsoft 365 connector"
    log_message "${WARNING}" "#   4. Follow the prompts to authenticate with your Microsoft account"
    log_message "${WARNING}" "#"
    log_message "${WARNING}" "# Reference: https://support.claude.ai/en/articles/12542951"
    log_message "${WARNING}" "#--------------------------------------------------------------------------------------------"
    echo
}
