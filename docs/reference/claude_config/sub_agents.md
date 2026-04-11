# 🤖 Sub-agents

Sub-agents are specialist personas that shape how Claude behaves in a session — what role it plays, what priorities it applies, and how it frames its responses. Each agent runs in its own context window with a focused system prompt, specific tool access, and independent permissions.

---

## 🎭 Core — full-session personas

Use these for open-ended sessions that span multiple technologies or concerns.

| Sub-agent | When to use |
|---|---|
| 🏛️ [Architect](../../src/claude/agents/core/architect.md) | End-to-end analytics architecture, hands-on SQL/Python/dbt work, ADRs, technical specs *(default)* |
| 📋 [Project manager](../../src/claude/agents/core/project_manager.md) | Work planning, stakeholder comms, sprint and backlog work |
| ✍️ [Technical writer](../../src/claude/agents/core/technical_writer.md) | Docs, READMEs, runbooks, ADRs, Confluence pages |

---

## 🔧 Utility — read-only review and diagnostics

Restricted to read-only tools. Use for review sessions or debugging without risk of file edits.

| Sub-agent | When to use |
|---|---|
| 🔍 [Code reviewer](../../src/claude/agents/utility/code_reviewer.md) | Holistic code review across all files — standards, security, test coverage |
| 🐛 [Debugger](../../src/claude/agents/utility/debugger.md) | Systematic root-cause debugging |

---

## ⚙️ Ops — Claude setup maintenance

Agents that operate on the Claude configuration itself, not on data or application code.

| Sub-agent | When to use |
|---|---|
| 🆕 [New user](../../src/claude/agents/ops/new_user.md) | Test the onboarding experience by simulating a first-time user |
| 🏅 [Claude reviewer](../../src/claude/agents/ops/claude_reviewer.md) | Review Claude configuration artefacts (agents, rules, skills) for quality and best practices |

---

## 🛠️ Tools — technology-specific agents

One agent per style guide. Use for focused work on a single technology, or for automated code review via hooks. When a task spans multiple technologies, use `architect` instead.

| Sub-agent | Owns | When to use |
|---|---|---|
| 🐍 [Python](../../src/claude/agents/tools/python.md) | `*.py` | Python code review and standards |
| 🗄️ [SQL](../../src/claude/agents/tools/sql.md) | `**/*.sql` | SQL / Snowflake query review |
| 🐚 [Unix](../../src/claude/agents/tools/unix.md) | `*.sh` | Bash/shell scripting review |
| 🔨 [Makefile](../../src/claude/agents/tools/makefile.md) | `Makefile`, `*.mk` | GNU Make conventions |
| 🔄 [dbt](../../src/claude/agents/tools/dbt.md) | `models/**/*.sql`, `models/**/*.yml` | dbt model review and test coverage |
| 🐳 [Docker](../../src/claude/agents/tools/docker.md) | `Dockerfile`, `.dockerignore` | Dockerfile security and optimisation |
| 🚀 [CI/CD](../../src/claude/agents/tools/cicd.md) | `.github/workflows/*.yml`, `azure-pipelines.yml` | Pipeline structure and deployment safety |
| ⚙️ [Ansible](../../src/claude/agents/tools/ansible.md) | `*.yml` (playbooks/roles) | Ansible playbook review |
| 🌊 [Airflow](../../src/claude/agents/tools/airflow.md) | `dags/**/*.py` | Airflow DAG review and idempotency |
| 🏗️ [Terraform](../../src/claude/agents/tools/terraform.md) | `*.tf`, `*.tfvars` | Terraform IaC review and module structure |

---

## 🏛️ Default: Architect

The `architect` persona loads by default when no sub-agent is specified in `session_input.md`. It is a planner-first persona for analytics work — it outlines approach, assumptions, and risks before making changes, and coordinates across the full data stack.

The `architect` and `technical_writer` agents also run with `isolation: worktree`, meaning they work in an isolated git worktree by default. See [worktrees.md](worktrees.md) for details.

---

## ⚙️ Hardcoding a sub-agent for a project

To skip the prompt and lock a sub-agent for a specific project, add an `@import` in a project-level `CLAUDE.md` at the repo root:

```markdown
@~/.claude/CLAUDE.md
@~/.claude/agents/tools/dbt.md
```
