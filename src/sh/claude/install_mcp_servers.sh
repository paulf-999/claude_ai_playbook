#!/bin/bash
set -e

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh
source src/sh/claude/helpers/mcp_helpers.sh
source src/sh/claude/helpers/mcp_server_installers.sh

#=======================================================================
# Functions
#=======================================================================

# Route to the appropriate install function based on the server argument
install_single_server() {
    local SERVER="$1"

    case "${SERVER}" in
        core)                                  # installs all core servers in one pass
            install_mcp_servers
            ;;
        context7)
            install_npx_server "context7" "${NPX_CONTEXT7}"
            ;;
        sequential-thinking)
            install_npx_server "sequential-thinking" "${NPX_SEQUENTIAL_THINKING}"
            ;;
        memory)
            install_npx_server "memory" "${NPX_MEMORY}"
            ;;
        filesystem)
            install_filesystem_server
            ;;
        github)                                # requires PAT — prompts interactively
            install_github_server
            ;;
        omni)                                  # requires OAuth — opens browser
            install_omni_server
            ;;
        atlassian)                             # requires SSO — opens browser
            install_atlassian_server
            ;;
        o365)                                  # cannot be scripted — prints manual instructions
            print_o365_reminder
            ;;
        *)
            log_message "${ERROR}" "Unknown server: '${SERVER}'. Valid options: core, context7, sequential-thinking, memory, filesystem, github, omni, atlassian, o365"
            exit 1
            ;;
    esac
}

#=======================================================================
# Main script logic
#=======================================================================

trap handle_interruption INT

print_section_header "${DEBUG}" "MCP server installation started."

install_single_server "${1:-}"

print_section_header "${DEBUG}" "MCP server installation completed."
