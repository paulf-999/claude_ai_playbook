SHELL = /bin/sh

#================================================================
# Usage
#================================================================
# make install                      # install Claude config files into ~/.claude/, install Claude CLI, and install core MCP servers
# make update                       # update Claude config files in ~/.claude/
# make install_claude_cli           # install Claude CLI via npm
# make install_core_mcp_servers     # install core MCP servers (context7, sequential-thinking, memory, filesystem)
# make install_mcp_server_github    # install GitHub MCP server (prompts for PAT)
# make install_mcp_server_atlassian # install Atlassian MCP server (opens browser for SSO)
# make install_mcp_server_o365      # print manual setup instructions for Microsoft 365 connector

#=======================================================================
# Variables
#=======================================================================
.EXPORT_ALL_VARIABLES:

# load variables from separate file
include src/make/variables.mk # load variables from a separate makefile file

#=======================================================================
# Targets
#=======================================================================
all: install

install:
	@echo "${INFO}\nInstalling Claude config files into ~/.claude/${COLOUR_OFF}"
	@bash src/sh/claude/install_claude_files.sh

update:
	@echo "${INFO}\nUpdating Claude config files in ~/.claude/${COLOUR_OFF}"
	@bash src/sh/claude/update_claude_files.sh

install_claude_cli:
	@echo "${INFO}\nInstalling Claude CLI${COLOUR_OFF}"
	@bash src/sh/claude/install_claude_cli.sh

install_core_mcp_servers:
	@echo "${INFO}\nInstalling core MCP servers${COLOUR_OFF}"
	@bash src/sh/claude/install_mcp_servers.sh core

install_mcp_server_github:
	@echo "${INFO}\nInstalling GitHub MCP server${COLOUR_OFF}"
	@bash src/sh/claude/install_mcp_servers.sh github

install_mcp_server_atlassian:
	@echo "${INFO}\nInstalling Atlassian MCP server${COLOUR_OFF}"
	@bash src/sh/claude/install_mcp_servers.sh atlassian

install_mcp_server_o365:
	@bash src/sh/claude/install_mcp_servers.sh o365

# Phony targets
.PHONY: all install update install_claude_cli install_core_mcp_servers install_mcp_server_github install_mcp_server_atlassian install_mcp_server_o365

# .PHONY tells Make that these targets don't represent files
# This prevents conflicts with any files named "all" or "clean"
