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
| ops | skill_auditor | `agents/ops/skill_auditor.md` |
| tools | python / sql / unix / makefile / dbt / docker / cicd / ansible / airflow / terraform / jira / payroc_engineering_naming_standards / codeowners *(one per style guide)* | `agents/tools/<name>.md` |
| pipeline *(files live in `core/`)* | data-project-manager / requirements-consolidator / payroc-data-architect / dbt-warehouse-engineer / dbt-pr-reviewer / dbt-uat-test-planner / dbt-uat-evaluator / data-docs-writer / airflow-dag-engineer / omni-semantic-engineer | `agents/core/<name>.md` |

Built-in Claude Code agents (no file needed): `general-purpose`, `explore`.

To switch sub-agent mid-session, just tell me which one to use.
