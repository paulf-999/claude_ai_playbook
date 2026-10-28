# Quality Scorecard — authoring_agents.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.4/10

**Recommended improvements:**
- Make the Quick Navigation step summary match the child: change "name → contract → AGENT.md → evals → score" to "name → frontmatter → AGENT.md → evals → document maturity".
- Remove "(below)" from "Hard Gates Checklist (below)" and point to `_hard_gates_checklist.md`, because the checklist is no longer in this file.
- Merge Quick Navigation into the Read on demand list, so each child is described once instead of twice.
- Rewrite the Purpose line as one sentence in British English ("standardised"), and change "finalizing" to "finalising".
- Change the Quick Navigation bullets from `**Keyword** —` to the house style `**Keyword:**`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-27 | • 🔍 **Audience routing:** the "new / experienced / reviewing" split tells each reader where to start<br>• ⚠️ **Dangling pointer:** line 30 says "Hard Gates Checklist (below)", but nothing below it is a checklist, only a pointer to a child file<br>• ⚠️ **Said twice:** Quick Navigation (lines 16–32) and Read on demand (lines 36–44) describe the same five children in different words |
| **Complexity** | 7/10 | 2026-10-27 | • 🧮 **Raw complexity 3:** Concepts 1 (audience navigation plus pointers) + Scope 2 (`rules/03_authoring_guidelines/` and `_rules_lazy_load/.../authoring_agents/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 7/10 | 2026-10-27 | • 🔗 **Recorded use:** the `test_authoring_agents.py` docstring records use in 2 of 115 sessions and a 2026-09-28 audit that found it had no test coverage<br>• 🔗 **Real agents:** `code_reviewer` and `technical_writer` both cite this rule in their References<br>• ⚠️ **Thin repeat use:** 2 of 115 sessions is the only usage figure, and no usage CSV or incident log backs it |
| **Token Cost Justification** | 9/10 | 2026-10-27 | • 🎯 **Path-scoped:** it sits in an always-on tier, but `paths: "**/agents/**"` makes it load only when an agent file is open<br>• 🎯 **Small parent:** 45 lines, with all detail in five on-demand children<br>• ✅ **Guarded:** `test_always_on_reachability.py` line 122 fails if it loads at startup again |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Within limits:** 45 lines, emoji H1, Purpose line, metadata header straight after the `paths:` frontmatter<br>• ⚠️ **Spelling:** "standardized" (line 12) and "finalizing" (line 22) break the British English rule<br>• ⚠️ **Two sentences:** the Purpose line (line 12) holds two sentences<br>• ⚠️ **Bullet style:** the Quick Navigation bullets use `**Keyword** —` instead of `**Keyword:**` |
| **Currency** | 6/10 | 2026-10-25 | • ✅ **Paths exist:** all five `Read on demand` children exist under `_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/`<br>• ⚠️ **Step drift:** line 21's "name → contract → AGENT.md → evals → score" doesn't match `_decision_tree_and_process.md` lines 52–56 (frontmatter, not contract, and "document maturity", not score)<br>• ⚠️ **Stale "(below)":** line 30 dates from before the checklist moved into a child |
| **Test Coverage** | 9/10 | 2026-10-27 | • 🧪 **Dedicated test:** `test_authoring_agents.py` checks every child pointer, that there are no `@import`s, that the children on disk match the expected list, the README parent entries, the `paths:` trigger and the pointer in `authoring_rules.md`<br>• 🧪 **Regression for real moves:** it guards the dated 2026-09-29 to 2026-10-06 location changes recorded in its docstring<br>• ⚠️ **Minor gap:** nothing checks that the Quick Navigation summaries match the children, which is how the step drift got through |
| **Overall** | **7.4/10** | 2026-10-27 | • 💪 **Lean, well-guarded index:** it loads only for agent files, and a dedicated test checks its structure<br>• ⚠️ **Stale navigation copy:** the duplicated Quick Navigation has drifted from the children it summarises |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/authoring_agents.md` — the rule being scored
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_decision_tree_and_process.md` — Currency (the 5 steps it disagrees with)
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Clarity and Currency (where the checklist actually lives)
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_agents.py` — Test Coverage and Evidence of Need
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Token Cost Justification
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/agents/core/code_reviewer/AGENT.md` — Evidence of Need
- `src/claude/agents/core/technical_writer/AGENT.md` — Evidence of Need
