# Global Claude configuration — composed from imports below.
# Source of truth: src/claude/CLAUDE.md in the playbook repo.
# Synced to ~/.claude/ via `make install` (run from environments/claude/dmt-scripts-claude_ai_playbook/).
# Do not edit ~/.claude/CLAUDE.md directly — changes will be overwritten on next install.

@~/.claude/process/environment.md
@~/.claude/process/planning.md
@~/.claude/process/session.md
@~/.claude/rules/behaviour/general.md
@~/.claude/rules/behaviour/risky_actions.md
@~/.claude/rules/development.md
@~/.claude/rules/git.md
@~/.claude/rules/file_standards.md
@~/.claude/rules/testing.md
@~/.claude/rules/security.md
@~/.claude/rules/integrations.md
@~/.claude/rules/cost_efficiency.md
@~/.claude/rules/transparency.md
@~/.claude/rules/optimisation.md
@~/.claude/rules/workflows.md
@~/.claude/style_guide_standards/datetime.md
@~/.claude/style_guide_standards/versioning.md
@~/.claude/style_guide_standards/python.md
@~/.claude/style_guide_standards/sql.md
@~/.claude/style_guide_standards/unix.md
@~/.claude/style_guide_standards/makefile.md
@~/.claude/style_guide_standards/dbt.md
@~/.claude/style_guide_standards/docker.md
@~/.claude/style_guide_standards/cicd.md
@~/.claude/style_guide_standards/ansible.md
@~/.claude/style_guide_standards/airflow.md
@~/.claude/style_guide_standards/terraform.md
@~/.claude/context.md

@./agents/core/architect.md

## Sub-agent selection

The `architect` sub-agent is loaded by default via the import above.

At the start of each session, read `~/.claude/process/session_input.md`. If the `## Sub-agent` section contains a non-comment value, load that sub-agent instead by importing the corresponding file from `~/.claude/agents/`. If no sub-agent is specified, continue with `architect`.

To override the default for a specific project, add an `@import` pointing to the desired agent file in a project-level `CLAUDE.md`.

Available sub-agents:

| Group | Agent | File |
|---|---|---|
| core | architect *(default)* | `agents/core/architect.md` |
| core | project_manager | `agents/core/project_manager.md` |
| core | technical_writer | `agents/core/technical_writer.md` |
| utility | code_reviewer | `agents/utility/code_reviewer.md` |
| utility | debugger | `agents/utility/debugger.md` |
| ops | new_user | `agents/ops/new_user.md` |
| ops | claude_reviewer | `agents/ops/claude_reviewer.md` |
| ops | mac_user | `agents/ops/mac_user.md` |
| tools | python / sql / unix / makefile / dbt / docker / cicd / ansible / airflow / terraform *(one per style guide)* | `agents/tools/<name>.md` |

Built-in Claude Code agents (no file needed): `general-purpose`, `explore`.

To switch sub-agent mid-session, just tell me which one to use.
