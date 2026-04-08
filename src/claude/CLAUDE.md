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

@./agents/dmt/architect.md

# The architect sub-agent is loaded by default.
# To use a different sub-agent for a specific project, override via @import in a project-level CLAUDE.md.
# Available sub-agents:
#   core/  (general purpose)
#     - core/code_reviewer.md
#     - core/debugger.md
#     - core/technical_writer.md
#     - core/devops.md
#   dmt/   (data management team)
#     - dmt/architect.md  (default)
#     - dmt/project_manager.md
#     - dmt/data_platform_architect.md
#     - dmt/data_engineer.md
#     - dmt/data_analyst.md
