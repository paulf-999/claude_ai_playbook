#!/bin/bash
set -e

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

MARKETPLACE="claude-plugins-official"
MARKETPLACE_SOURCE="anthropics/claude-plugins-official"

# Plugins to install from the official marketplace
PLUGINS=(
    "ralph-loop"
    "security-guidance"
    "skill-creator"
    "claude-md-management"
    "pyright-lsp"
)

#=======================================================================
# Functions
#=======================================================================

# Return 0 if the marketplace is already configured, 1 otherwise
is_marketplace_registered() {
    claude plugin marketplace list 2>/dev/null | grep -q "${MARKETPLACE}"
}

# Return 0 if a plugin is already installed, 1 otherwise
is_plugin_installed() {
    local PLUGIN_NAME="$1"
    claude plugin list --json 2>/dev/null | grep -q "\"${PLUGIN_NAME}@"
}

# Add the official Anthropic plugin marketplace if not already present
ensure_marketplace() {
    if is_marketplace_registered; then
        log_message "${INFO}" "Skipping marketplace '${MARKETPLACE}' — already registered."
    else
        log_message "${DEBUG}" "Adding marketplace '${MARKETPLACE}'..."
        claude plugin marketplace add "${MARKETPLACE_SOURCE}"
        log_message "${INFO}" "Added marketplace '${MARKETPLACE}'."
    fi
}

# Install a single plugin by name
install_plugin() {
    local PLUGIN_NAME="$1"

    if is_plugin_installed "${PLUGIN_NAME}"; then
        log_message "${INFO}" "Skipping '${PLUGIN_NAME}' — already installed."
    else
        log_message "${DEBUG}" "Installing '${PLUGIN_NAME}'..."
        claude plugin install "${PLUGIN_NAME}"
        log_message "${INFO}" "Installed '${PLUGIN_NAME}'."
    fi
}

# Install all plugins defined in PLUGINS
install_all_plugins() {
    for PLUGIN in "${PLUGINS[@]}"; do
        install_plugin "${PLUGIN}"
    done
}

#=======================================================================
# Main script logic
#=======================================================================

print_section_header "${DEBUG}" "Plugin installation started."

ensure_marketplace
install_all_plugins

log_message "${INFO}" "Pyright LSP requires pyright to be installed separately:"
log_message "${INFO}" "  pip install pyright    (or: pipx install pyright)"

print_section_header "${DEBUG}" "Plugin installation completed."
