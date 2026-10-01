# Quality Scorecard — behaviour.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.7/10

**Recommended improvements:**
- Add dedicated structural tests for the 5 untested children: `_how_to_approach.md`, `_before_acting.md`, `_pre_existing_issue_disclosure.md`, `_model_selection_strategy.md`, `_session_conduct.md`.
- Document a clear criterion for when a behavioral concept is promoted to its own child file versus kept inline in the parent.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-28 | • 📋 **Comprehensive:** covers proposing, acting, risky actions, and decision-making with concrete examples<br>• 🔍 **Mixed structure:** some concepts are inline (Before Claiming Completion, Risky Actions), others delegated to 7 children — no obvious rule for which |
| **Complexity** | 6/10 | 2026-09-28 | • 🧮 **Raw complexity 4:** 6+ distinct behavioral concepts across inline content and 7 imported children — the most fanned-out parent in this survey |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Most cross-referenced rule in the config:** cited by name across nearly every other rule file touched this session |
| **Token Cost Justification** | 10/10 | 2026-09-28 | • 🎯 **Scope:** Tier 2, always-on, blocking/safety-critical — governs every risky or ambiguous action |
| **Structural Compliance** | 7/10 | 2026-09-28 | • ✅ **Compliant:** emoji headers, Purpose statement, trailing newline<br>• 🌳 **Fan-out inconsistency:** 7 children plus 3 inline sections that are arguably equally weighty — no clear line between what got promoted to a child file and what didn't |
| **Currency** | 8/10 | 2026-09-28 | • 🔍 **Check:** no stale references found in the parent's own inline content |
| **Test Coverage** | 6/10 | 2026-09-28 | • 🧪 **Partial:** only 2 of 7 children have dedicated tests (`test_decision_making.py`, `test_artefact_proposal_gates.py`)<br>• ⚠️ **Untested children:** `_how_to_approach.md`, `_before_acting.md`, `_pre_existing_issue_disclosure.md`, `_model_selection_strategy.md`, `_session_conduct.md` have no dedicated test file |
| **Overall** | **7.7/10** | 2026-09-28 | • 💪 **Strength:** the config's most load-bearing safety rule, heavily and correctly followed in practice<br>• ⚠️ **Gap:** 5 of 7 children rely solely on generic structural checks |

## 🔗 Related files

- `src/claude/_rules/02_claude_standards/behaviour.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_decision_making.py` — Test Coverage dimension
- `src/claude/_tests/rules/02_claude_standards/test_artefact_proposal_gates.py` — Test Coverage dimension
- `src/claude/_rules/02_claude_standards/behaviour/_how_to_approach.md` — Test Coverage dimension (untested child)
- `src/claude/_rules/02_claude_standards/behaviour/_before_acting.md` — Test Coverage dimension (untested child)
- `src/claude/_rules/02_claude_standards/behaviour/_pre_existing_issue_disclosure.md` — Test Coverage dimension (untested child)
- `src/claude/_rules/02_claude_standards/behaviour/_model_selection_strategy.md` — Test Coverage dimension (untested child)
- `src/claude/_rules/02_claude_standards/behaviour/_session_conduct.md` — Test Coverage dimension (untested child)
