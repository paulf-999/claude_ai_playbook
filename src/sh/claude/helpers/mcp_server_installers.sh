#!/bin/bash

# Server-specific MCP installation functions

# Install the GitHub MCP server via remote HTTP (requires a GitHub PAT with repo scope)
install_github_server() {
    if is_installed "github"; then
        log_message "${INFO}" "Skipping 'github' — already registered."
        verify_installation "github"
        return
    fi

    echo
    log_message "${WARNING}" "The GitHub MCP server requires a Personal Access Token (PAT) with 'repo' scope."
    log_message "${WARNING}" "Create one at: https://github.com/settings/personal-access-tokens/new"
    echo
    read -r -s -p "Enter your GitHub PAT (input is hidden): " GITHUB_PAT  # -s suppresses echo for security
    echo

    if [[ -z "${GITHUB_PAT}" ]]; then
        log_message "${WARNING}" "No PAT provided — skipping 'github' MCP server."
        return
    fi

    log_message "${DEBUG}" "Installing 'github' MCP server (remote HTTP)..."
    claude mcp add-json github \
        "{\"type\":\"http\",\"url\":\"https://api.githubcopilot.com/mcp\",\"headers\":{\"Authorization\":\"Bearer ${GITHUB_PAT}\"}}" \  # PAT injected at runtime, never stored
        --scope user
    log_message "${INFO}" "Installed 'github'."

    verify_installation "github"
}

# Install the Atlassian MCP server via HTTP transport (triggers OAuth/SSO in browser)
install_atlassian_server() {
    if is_installed "atlassian"; then
        log_message "${INFO}" "Skipping 'atlassian' — already registered."
        verify_installation "atlassian"
        return
    fi

    log_message "${DEBUG}" "Installing 'atlassian' (HTTP transport — will open browser for SSO)..."
    claude mcp add --scope user --transport http atlassian https://mcp.atlassian.com/v1/mcp  # SSO handled by browser redirect
    log_message "${INFO}" "Installed 'atlassian'."
    verify_installation "atlassian"
}

# Install core MCP servers (no authentication required)
install_mcp_servers() {
    for NAME in "${!NPX_SERVERS[@]}"; do
        install_npx_server "${NAME}" "${NPX_SERVERS[${NAME}]}"  # look up command by server name
    done

    install_filesystem_server
}
