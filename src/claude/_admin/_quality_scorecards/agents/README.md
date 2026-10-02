# 🤖 Agent Scorecards

**Purpose:** Home for agent quality scorecards — one per `AGENT.md` under `agents/`, scored on seven dimensions adapted to what makes an agent good.

---

## 📁 Location convention

One file per agent, named after it: `_admin/_quality_scorecards/agents/scorecard_<agent_name>.md`.

- **Example:** `agents/core/technical_writer/AGENT.md` → `scorecard_technical_writer.md`
- **Never `@import` these files:** they're review records, not content Claude reads while working.

---

## 📋 Template

Use the shared `_templates/scorecard.md.template` with these seven dimensions, in this order.

---

## 🎯 Per-dimension criteria

| Dimension | 10 looks like | 1 looks like |
|---|---|---|
| **Clarity** | The description says exactly when to use the agent, with triggers a user would actually type | Vague description, so it's picked at the wrong times or never |
| **Scope Boundaries** | An explicit "not for" list, and no overlap with a skill or another agent | Does the same job as an existing skill or agent |
| **Complexity** | Inverted shared formula (`03_authoring_guidelines/shared_standards/_complexity_scoring.md`): one concept, no external services | Several jobs and several required integrations |
| **Evidence of Need** | Handles a real task that recurs, with usage recorded | Built for a hypothetical, with no record of use |
| **Test Coverage** | Structured evals that cover triggering, output and the "not for" cases, at the count its maturity needs | No evals, or prose scenarios nothing runs |
| **Structural Compliance** | Passes every item in `authoring_agents/_lazy_load/_hard_gates_checklist.md` | Missing frontmatter, sections or metadata header |
| **Tool Safety** | A `tools:` allowlist limited to what the job needs, plus worktree isolation if it writes files | Every tool available, with no isolation |

**Overall:** the average of the seven dimensions, rounded to one decimal place.

---

## 📅 When to score

- **On creation:** every new agent gets a scorecard alongside it.
- **On re-score:** when an agent's scope, tools or maturity changes, update its scorecard.
- **Summary:** update the agent's row in `agent_scorecards_summary.md` in the same commit.
