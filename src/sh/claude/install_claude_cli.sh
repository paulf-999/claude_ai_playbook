#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status (fail fast).

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

#=======================================================================
# Functions
#=======================================================================

# Source nvm if it is installed but not active in the current subshell.
# When scripts run as 'bash script.sh', .bashrc/.zshrc is not sourced,
# so nvm shell functions are absent even if nvm is installed.
maybe_source_nvm() {
    local NVM_SCRIPT="${NVM_DIR:-${HOME}/.nvm}/nvm.sh"
    if [[ -s "${NVM_SCRIPT}" ]]; then
        # shellcheck source=/dev/null
        source "${NVM_SCRIPT}"
        log_message "${DEBUG_DETAILS}" "Sourced nvm from ${NVM_SCRIPT}"
    fi
}

# Install nvm and Node.js LTS via the official nvm install script.
# nvm v0.40.3 — update this version pin periodically.
install_nvm_and_node() {
    log_message "${INFO}" "npm not found — installing nvm and Node.js LTS..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

    local NVM_SCRIPT="${HOME}/.nvm/nvm.sh"
    if [[ ! -s "${NVM_SCRIPT}" ]]; then
        log_message "${WARNING}" "nvm installation failed — skipping Claude CLI installation."
        return 1
    fi

    # shellcheck source=/dev/null
    source "${NVM_SCRIPT}"
    nvm install --lts
    nvm use --lts
}

# Attempt to refresh PATH after a global npm install so the new binary is
# immediately visible without opening a new terminal. Tries three approaches
# in order: re-source nvm (most common case), Homebrew shell env (macOS), and
# a command-hash reset. Safe to call even if none of the tools are present.
refresh_path_after_install() {
    maybe_source_nvm
    if command -v brew &>/dev/null; then
        eval "$(brew shellenv)" 2>/dev/null || true
    fi
    hash -r 2>/dev/null || true
}

# Return non-zero if the npm global prefix directory is not user-writable.
# A non-writable prefix indicates system-managed npm (e.g. apt, official pkg
# installer) where 'npm install -g' requires sudo.
check_npm_prefix_writable() {
    local NPM_PREFIX
    NPM_PREFIX=$(npm config get prefix)
    if [[ ! -w "${NPM_PREFIX}" ]]; then
        log_message "${WARNING}" "npm global prefix '${NPM_PREFIX}' is not user-writable (system-managed npm)."
        log_message "${WARNING}" "Use nvm for permission-free global installs: https://github.com/nvm-sh/nvm"
        return 1
    fi
}

# Install the Claude CLI, handling Node.js/npm prerequisites automatically.
install_claude_cli() {
    if command -v claude &>/dev/null; then
        log_message "${INFO}" "Claude CLI already installed — skipping."
        return 0
    fi

    # nvm may be installed but not active in this non-interactive subshell
    maybe_source_nvm

    if ! command -v npm &>/dev/null; then
        install_nvm_and_node
    fi

    # Guard: if npm is still not available after the install attempt, abort
    if ! command -v npm &>/dev/null; then
        log_message "${WARNING}" "npm unavailable — skipping Claude CLI installation."
        return 0
    fi

    # Guard: abort if the npm prefix is not user-writable
    if ! check_npm_prefix_writable; then
        return 0
    fi

    log_message "${INFO}" "Installing Claude CLI..."
    npm install -g @anthropic-ai/claude-code

    # The install may not be visible in PATH yet — attempt a targeted refresh
    # before falling back to a message.
    if ! command -v claude &>/dev/null; then
        refresh_path_after_install
    fi

    if command -v claude &>/dev/null; then
        log_message "${INFO}" "Claude CLI installed successfully."
    else
        log_message "${WARNING}" "Claude CLI installed but not yet in PATH. Open a new terminal or run: source ~/.nvm/nvm.sh"
    fi
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "Claude CLI installation started."

install_claude_cli

print_section_header "${DEBUG}" "Claude CLI installation completed." && echo
