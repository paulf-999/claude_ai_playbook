#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status (fail fast).

# Load reusable shell script vars & functions
source src/sh/claude/helpers/claude_file_utils.sh

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

# Install the Claude CLI via npm (optional step — failure does not abort the install)
install_claude_cli() {
    bash src/sh/claude/install_claude_cli.sh \
        || log_message "${WARNING}" "Claude CLI installation did not complete — run: bash src/sh/claude/install_claude_cli.sh"
}

# Add the npm global bin directory to PATH for the remainder of this script.
# Required so that install_core_mcp_servers and install_plugins can find the
# newly installed claude binary without the user opening a new terminal.
update_npm_path() {
    local NPM_PREFIX
    NPM_PREFIX=$(npm config get prefix 2>/dev/null) || return 0
    if [ -n "$NPM_PREFIX" ] && [[ ":$PATH:" != *":$NPM_PREFIX/bin:"* ]]; then
        export PATH="$NPM_PREFIX/bin:$PATH"
        log_message "${DEBUG}" "Added $NPM_PREFIX/bin to PATH for this session."
    fi
}

# Install core MCP servers (optional step — failure does not abort the install)
# Skips gracefully if the claude CLI is not yet installed.
install_core_mcp_servers() {
    if ! command -v claude &>/dev/null; then
        log_message "${WARNING}" "Claude CLI not found — skipping MCP server installation."
        log_message "${WARNING}" "Run: make install_core_mcp_servers"
        return 0
    fi
    bash src/sh/claude/install_mcp_servers.sh core \
        || log_message "${WARNING}" "MCP server installation did not complete — run: make install_core_mcp_servers"
}

# Install Claude Code plugins (optional step — failure does not abort the install)
# Skips gracefully if the claude CLI is not yet installed.
install_plugins() {
    if ! command -v claude &>/dev/null; then
        log_message "${WARNING}" "Claude CLI not found — skipping plugin installation."
        log_message "${WARNING}" "Run: bash src/sh/claude/install_plugins.sh"
        return 0
    fi
    bash src/sh/claude/install_plugins.sh \
        || log_message "${WARNING}" "Plugin installation did not complete — run: bash src/sh/claude/install_plugins.sh"
}

# Print instructions for optional MCP servers that require manual setup
print_optional_mcp_instructions() {
    print_section_header "${INFO}" "Optional MCP servers — run these commands to install when ready" && echo
    echo "  GitHub        (requires a PAT with 'repo' scope)"
    echo "    bash src/sh/claude/install_mcp_servers.sh github"
    echo
    echo "  Atlassian     (requires SSO — opens browser)"
    echo "    bash src/sh/claude/install_mcp_servers.sh atlassian"
    echo
    echo "  Microsoft 365 (Claude web UI only — cannot be configured via CLI)"
    echo "    bash src/sh/claude/install_mcp_servers.sh o365"
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Claude file installation started."

install_claude_files
print_operation_summary "installation"
install_claude_cli
update_npm_path
install_core_mcp_servers
install_plugins
print_optional_mcp_instructions

print_section_header "${DEBUG}" "Claude file installation completed." && echo
