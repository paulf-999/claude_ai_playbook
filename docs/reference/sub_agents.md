# 🤖 Sub-agents

Sub-agents are specialist personas that shape how Claude behaves in a session — what role it plays, what priorities it applies, and how it frames its responses.

---

## 🏢 Data Management team

These agents carry context about the team's stack and working practices.

| Sub-agent | When to use |
|---|---|
| 📋 [Project manager](../src/claude/agents/dmt/project_manager.md) | Planning, documentation, stakeholder communication |
| 🏗️ [Data platform architect](../src/claude/agents/dmt/data_platform_architect.md) | Architecture decisions, tool selection, technical design |
| ⚙️ [Data engineer](../src/claude/agents/dmt/data_engineer.md) | Pipeline development, dbt, Python, Snowflake |
| 📊 [Data analyst](../src/claude/agents/dmt/data_analyst.md) | SQL queries, data investigation, reporting |

## 🔧 General purpose

These agents are domain-agnostic and available across all projects.

| Sub-agent | When to use |
|---|---|
| 🔍 [Code reviewer](../src/claude/agents/core/code_reviewer.md) | Code review, quality, standards enforcement |
| 🐛 [Debugger](../src/claude/agents/core/debugger.md) | Structured debugging sessions |
| ✍️ [Technical writer](../src/claude/agents/core/technical_writer.md) | Docs, READMEs, runbooks, PR descriptions |
| 🚀 [DevOps](../src/claude/agents/core/devops.md) | CI/CD, infrastructure, scripting |

---

## 🏛️ Default: Architect

The [Architect](../src/claude/agents/dmt/architect.md) persona loads by default. It is a planner-first persona designed for analytics work — it outlines approach, assumptions, and risks before making any changes, and coordinates across the full data stack. Claude will ask which sub-agent to use at the start of every session; if no override is selected, Architect is used.

---

## ⚙️ Hardcoding a sub-agent for a project

To skip the prompt and lock a sub-agent for a specific project, add an `@import` in a project-level `CLAUDE.md` at the repo root:

```markdown
@~/.claude/CLAUDE.md
@~/.claude/agents/dmt/data_engineer.md
```
