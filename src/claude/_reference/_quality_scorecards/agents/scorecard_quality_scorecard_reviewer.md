# Quality Scorecard — quality_scorecard_reviewer

**Date Created:** 2026-10-22
**Date Updated:** 2026-10-22

**Overall score:** 8.6/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-10-22 | • 🔍 **Description:** says what it scores, why it runs in a fresh context and that it's read-only<br>• 🎯 **Triggers:** a slash command plus three phrases that name the job, such as "score this skill, rule or agent" |
| **Scope Boundaries** | 10/10 | 2026-10-22 | • ✅ **Distinct job:** scores one artefact, while `code_reviewer` reviews diffs and `claude_review_config` audits the config<br>• ✅ **Not-for list:** hooks, tests, PR diffs and whole-config audits |
| **Complexity** | 7/10 | 2026-10-22 | • 🧮 **Raw complexity 3:** one scoring job (Concepts 1), reads artefacts and rubrics across folders (Scope 2), no external services |
| **Evidence of Need** | 6/10 | 2026-10-22 | • ✅ **Real problem:** issue #381 shows authors scoring their own work in the same context<br>• ⚠️ **No runs yet:** nothing in `score_history.csv` records it being used |
| **Test Coverage** | 7/10 | 2026-10-22 | • 📊 **Count:** 7 structured evals, within the draft range, covering triggering, scoring and every "not for" case<br>• ⚠️ **Not run:** nothing executes them yet, which caps this dimension at 7 |
| **Structural Compliance** | 10/10 | 2026-10-22 | • ✅ **Hard gates:** frontmatter, metadata header, all five sections and a Maturity Justification<br>• ✅ **Length:** 60 lines, within the ~40-60 guide |
| **Tool Safety** | 10/10 | 2026-10-22 | • 🔒 **Allowlist:** Read, Grep and Glob only, with no Bash, Write or MCP<br>• ✅ **Isolation:** none, which fits an agent that never writes files |
| **Overall** | **8.6/10** | 2026-10-22 | • 💪 **Strongest:** Clarity, Scope Boundaries, Structural Compliance and Tool Safety (10/10)<br>• ⚠️ **Weakest:** Evidence of Need (6/10) |

## 🔗 Related files

- `src/claude/agents/core/quality_scorecard_reviewer/AGENT.md` — the agent being scored
- `src/claude/agents/core/quality_scorecard_reviewer/evals.yaml` — Test Coverage dimension
- `src/claude/agents/core/code_reviewer/AGENT.md` — Scope Boundaries dimension
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance dimension
