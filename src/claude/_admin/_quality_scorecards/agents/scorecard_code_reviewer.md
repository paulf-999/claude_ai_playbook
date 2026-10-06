# Quality Scorecard — code_reviewer

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-05

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-10-05 | • 🔍 **Description:** says what it reviews, what it returns and that it's read-only<br>• 🎯 **Triggers:** a slash command plus four phrases people type, such as "review my changes" |
| **Scope Boundaries** | 10/10 | 2026-10-05 | • ✅ **Distinct job:** reviews only, while `git_review_pr` owns PR reviews and posting<br>• ✅ **No overlap:** no shared triggers with any skill, and bug hunts go to the built-in `/code-review` skill |
| **Complexity** | 8/10 | 2026-10-05 | • 🧮 **Raw complexity 2:** one review job (Concepts 1), reads the change and nearby context (Scope 1), no external services |
| **Evidence of Need** | 6/10 | 2026-10-05 | • ✅ **Real use:** needed on 2026-10-05 to review an infrastructure PR through `git_review_pr`<br>• ⚠️ **One use:** no wider usage record yet |
| **Test Coverage** | 8/10 | 2026-10-05 | • 📊 **Count:** 8 structured evals, the draft maximum, covering triggering, output and every "not for" case<br>• ⚠️ **Not run:** nothing executes them yet |
| **Structural Compliance** | 10/10 | 2026-10-05 | • ✅ **Hard gates:** frontmatter, metadata header, all five sections and a Maturity Justification<br>• ✅ **Constraints:** "Does NOT" lines, each with its reason |
| **Tool Safety** | 10/10 | 2026-10-05 | • 🔒 **Allowlist:** Read, Grep and Glob only, with no Bash, Write or MCP<br>• ✅ **Isolation:** none, which fits an agent that never writes files |
| **Overall** | **8.9/10** | 2026-10-05 | • 💪 **Strongest:** Clarity, Scope Boundaries, Structural Compliance and Tool Safety (10/10)<br>• ⚠️ **Weakest:** Evidence of Need (6/10) |

## 🔗 Related files

- `src/claude/agents/core/code_reviewer/AGENT.md` — the agent being scored
- `src/claude/agents/core/code_reviewer/evals.yaml` — Test Coverage dimension
- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — Scope Boundaries dimension
- `src/claude/_rules_lazy_load/authoring_guidelines/authoring_agents/_hard_gates_checklist.md` — Structural Compliance dimension
