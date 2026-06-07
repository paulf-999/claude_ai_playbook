#================================================================
# MCP server targets
#
# Included by the root Makefile. Contains standalone targets for
# individual MCP server installs and session-level enable/disable.
# Core MCP servers and plugins are installed automatically by
# make install — these targets exist for re-runs or targeted installs.
#
# Usage:
#   make install_core_mcp_servers     # install core MCP servers (context7, sequential-thinking, memory, filesystem)
#   make install_mcp_server_github    # install GitHub MCP server (prompts for PAT)
#   make install_mcp_server_omni      # install Omni Analytics MCP server (opens browser for OAuth)
#   make install_mcp_server_atlassian # install Atlassian MCP server (opens browser for SSO)
#   make install_mcp_server_o365      # print manual setup instructions for Microsoft 365 connector
#   make enable_mcp server=<name>     # enable an integration MCP server (groups: dev, docs, all)
#   make disable_mcp server=<name>    # disable an integration MCP server (groups: dev, docs, all)
#================================================================

install_core_mcp_servers:
	@echo "${INFO}\nInstalling core MCP servers${COLOUR_OFF}"
	@bash src/sh/claude/install_mcp_servers.sh core

install_mcp_server_github:
	@echo "${INFO}\nInstalling GitHub MCP server${COLOUR_OFF}"
	@bash src/sh/claude/install_mcp_servers.sh github

install_mcp_server_omni:
	@echo "${INFO}\nInstalling Omni Analytics MCP server${COLOUR_OFF}"
	@bash src/sh/claude/install_mcp_servers.sh omni

install_mcp_server_atlassian:
	@echo "${INFO}\nInstalling Atlassian MCP server${COLOUR_OFF}"
	@bash src/sh/claude/install_mcp_servers.sh atlassian

install_mcp_server_o365:
	@bash src/sh/claude/install_mcp_servers.sh o365

enable_mcp:
	@echo "${INFO}\nEnabling MCP server: $(server)${COLOUR_OFF}"
	@bash src/sh/claude/mcp_toggle.sh enable $(server)

disable_mcp:
	@echo "${INFO}\nDisabling MCP server: $(server)${COLOUR_OFF}"
	@bash src/sh/claude/mcp_toggle.sh disable $(server)

.PHONY: install_core_mcp_servers install_mcp_server_github install_mcp_server_omni install_mcp_server_atlassian install_mcp_server_o365 enable_mcp disable_mcp
