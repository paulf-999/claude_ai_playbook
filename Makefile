SHELL = /bin/sh

#================================================================
# Usage
#================================================================
# make deps             # install Python test dependencies into the active environment
# make test             # run structural validation tests
# make lint_tags        # validate Tier 1 tags on all Claude components (run before committing)
# make audit_components # run periodic health audit on the Claude component library
# make install          # install Claude config files, Claude CLI, core MCP servers, and plugins
# make update           # update Claude config files in ~/.claude/
# make install_plugins  # install Claude Code plugins only (runs install_plugins.sh)
# make patch_plugins    # apply team patches to installed plugins (run after install_plugins)
#
# MCP server targets (install_core_mcp_servers, install_mcp_server_*, enable_mcp,
# disable_mcp) are defined in src/make/mcp.mk.
#================================================================

#=======================================================================
# Variables
#=======================================================================
include src/make/variables.mk
include src/make/mcp.mk

#=======================================================================
# Targets
#=======================================================================
all: install

deps:
	@echo "${INFO}\nInstalling Python test dependencies${COLOUR_OFF}"
	@pip install -r requirements.txt

install:
	@echo "${INFO}\nInstalling Claude config files into ~/.claude/${COLOUR_OFF}"
	@bash src/sh/claude/install_claude_files.sh

update:
	@echo "${INFO}\nUpdating Claude config files in ~/.claude/${COLOUR_OFF}"
	@bash src/sh/claude/update_claude_files.sh

install_plugins:
	@echo "${INFO}\nInstalling Claude Code plugins${COLOUR_OFF}"
	@bash src/sh/claude/install_plugins.sh

patch_plugins:
	@echo "${INFO}\nApplying team patches to installed plugins${COLOUR_OFF}"
	@python3 src/claude/skills/patches/skill-creator-patch.py

test:
	@echo "${INFO}\nRunning structural validation tests${COLOUR_OFF}"
	@pytest

lint_tags:
	@echo "${INFO}\nValidating Tier 1 tags on Claude components${COLOUR_OFF}"
	@python3 src/sh/claude/claude_tag_lint.py

audit_components:
	@echo "${INFO}\nRunning Claude component health audit${COLOUR_OFF}"
	@python3 src/sh/claude/claude_component_audit.py

# .PHONY tells Make that these targets don't represent files
.PHONY: all deps install update install_plugins patch_plugins test lint_tags audit_components
