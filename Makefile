SHELL = /bin/bash

#================================================================
# Usage
#================================================================
# make deps             # install Python test dependencies into the active environment
# make test             # run structural validation tests
# make lint_tags        # validate Tier 1 tags on all Claude components (run before committing)
# make audit_components # run periodic health audit on the Claude component library
# make audit_rule_usage # measure how often each rule applies and loads, from session transcripts
# make install          # install Claude config files into $CLAUDE_CONFIG_DIR (previews, then asks you to type 'install')
# make update           # [DISABLED] update Claude config files in ~/.claude/ (WSL)
# make clean_plans      # archive executed/superseded plans to ~/.claude/plans/archive/
# make clean_backups    # move old ~/.claude_backup_* dirs to ~/.claude_backup_archive/
# make clean            # run clean_plans and clean_backups
# make all              # print this usage list
# make install_windows  # sync Claude config files to Windows .claude (run from WSL2)
# make update_windows   # alias for install_windows
# make sync             # [DISABLED] update WSL + Windows .claude in one step (run from WSL2)
# make install_plugins  # install Claude Code plugins only (runs install_plugins.sh)
# make patch_plugins    # apply team patches to installed plugins (run after install_plugins)
#
# MCP server targets (install_core_mcp_servers, install_mcp_server_*, enable_mcp)
# are defined in src/make/mcp.mk.
#================================================================

#=======================================================================
# Variables
#=======================================================================
include src/make/variables.mk
include src/make/mcp.mk

#=======================================================================
# Targets
#=======================================================================
deps:
	@echo "${INFO}\nInstalling Python test dependencies${COLOUR_OFF}"
	@pip install -r requirements.txt

install:
	@echo "${INFO}\nInstalling Claude config files into \$$CLAUDE_CONFIG_DIR${COLOUR_OFF}"
	@bash src/sh/claude/install_claude_files.sh

# update:
# 	@echo "${INFO}\nUpdating Claude config files in ~/.claude/${COLOUR_OFF}"
# 	@bash src/sh/claude/update_claude_files.sh

install_windows:
	@echo "${INFO}\nSyncing Claude config files to Windows .claude (requires WSL2)${COLOUR_OFF}"
	@bash src/sh/claude/install_claude_files_windows.sh

update_windows: install_windows

# sync: update_windows

install_plugins:
	@echo "${INFO}\nInstalling Claude Code plugins${COLOUR_OFF}"
	@bash src/sh/claude/install_plugins.sh

patch_plugins:
	@echo "${INFO}\nApplying team patches to installed plugins${COLOUR_OFF}"
	@python3 src/claude/plugins/skill-creator-patch.py

test:
	@echo "${INFO}\nRunning structural validation tests${COLOUR_OFF}"
	@pytest

lint_tags:
	@echo "${INFO}\nValidating Tier 1 tags on Claude components${COLOUR_OFF}"
	@python3 src/claude/_scripts/_lint_scripts/lint_claude_tags.py

lint_skills:
	@echo "${INFO}\nValidating skill authoring gate (crawl criteria)${COLOUR_OFF}"
	@python3 src/claude/_scripts/_lint_scripts/lint_skill_authoring_gate.py

lint: lint_tags lint_skills
	@echo "${INFO}\nLinting complete${COLOUR_OFF}"

audit_components:
	@echo "${INFO}\nRunning Claude component health audit${COLOUR_OFF}"
	@python3 src/claude/_scripts/_audit_scripts/audit_claude_component.py src/claude

audit_rule_usage:
	@echo "${INFO}\nMeasuring rule usage from session transcripts${COLOUR_OFF}"
	@python3 src/claude/_scripts/_audit_scripts/audit_rule_usage.py \
		--rules src/claude/_rules \
		--transcripts "$${CLAUDE_CONFIG_DIR:-$$HOME/.claude}/projects" \
		--out src/claude/_admin/_audits

clean_plans:
	@echo "${INFO}\nArchiving executed/superseded plans to ~/.claude/plans/archive/${COLOUR_OFF}"
	@python3 src/claude/_scripts/_clean_scripts/clean_plans.py

clean_backups:
	@echo "${INFO}\nMoving old ~/.claude_backup_* dirs to ~/.claude_backup_archive/${COLOUR_OFF}"
	@python3 src/claude/_scripts/_clean_scripts/clean_backups.py

clean: clean_plans clean_backups

# Print the usage block (kept last so `make` alone still runs deps)
all:
	@grep -E '^# make ' Makefile

# .PHONY tells Make that these targets don't represent files
.PHONY: all clean deps install install_windows update_windows install_plugins patch_plugins test lint lint_tags lint_skills audit_components audit_rule_usage clean_plans clean_backups
