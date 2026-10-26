# Quality Scorecard — authoring_rules.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.0/10

**Recommended improvements:**
- Name the file to open in line 37's naming pointer
- Make line 51's test location agree with the hard gates (`_tests/rules/` or `_tests/hooks/`)
- Give the checklist sub-bullets bold keywords and use British spelling on lines 9 and 52
- Reconcile the always-on placement with the narrow `applies_to` on line 4

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear process:** the checklist, five creation steps and quality gates are easy to follow in order.<br>• ⚠️ **Muddled pointer:** `authoring_rules.md` line 37 ("naming via `naming_standards.md` → children files for directory structure and naming patterns") doesn't say which file to open.<br>• ⚠️ **Test location conflict:** line 51 says enforcement tests go in `_tests/rules/`, but `_hard_gates_checklist.md` line 31 allows `_tests/rules/` or `_tests/hooks/`. |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (pre-creation checklist, creation steps, quality gates, common mistakes, lifecycle) + Scope 2 (`rules/`, `_rules_lazy_load/`, `_tests/`, `_templates/`, `_reference/`) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Wide reach:** lines 47–52 and 63–66 send the author into five folders. |
| **Evidence of Need** | 8/10 | 2026-10-25 | • 🔗 **Recorded mistakes:** `_common_mistakes.md` cites PR #94 (lines 33–37), PR #97 (line 57) and the 2026-09-17 portable-path incidents (line 27).<br>• ⚠️ **None in the parent:** `authoring_rules.md` lines 9–11 claim a need but record no incident or usage. |
| **Token Cost Justification** | 6/10 | 2026-10-25 | • 🎯 **Reason given:** line 6 explains always-on loading (a new rule can start before any rule file is open), and the bulky children are on demand (lines 75–77).<br>• ⚠️ **Scope mismatch:** line 4's `applies_to: **/rules/**, **/_rules_lazy_load/**` names a narrow set of files, yet the rule loads in every session, which is near the ~5 anchor ("always-on, but only one file type's sessions need it"). |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Basics met:** 78 lines, metadata header on lines 1–6, an emoji H1, a Purpose line and the bulky children split out.<br>• ⚠️ **Plain sub-bullets:** lines 18–19, 22–25, 28–29, 32–34 and 37–43 don't open with a bold keyword, which fails the `_hard_gates_checklist.md` line 25 gate.<br>• ⚠️ **Multi-sentence item:** line 51 holds two sentences.<br>• ⚠️ **American spelling:** "standardized" and "rigor" on line 9 and "centralized" on line 52 break the house rule of British spelling. |
| **Currency** | 8/10 | 2026-10-25 | • 🔍 **Paths exist:** the template, `testing.md`, `test_rules_structure.py`, `test_always_on_reachability.py`, `claude_rule_loading_strategy.md`, `authoring_agents.md`, the reviewer agent and `score_history.csv` are all on disk.<br>• ⚠️ **Unmeasured figure:** line 22's "~100–150 tokens/session cost" is a fixed estimate, while `claude_rule_loading_strategy.md` says `make audit_rule_usage` reports the measured sizes.<br>• ⚠️ **Partial drift:** line 51's `_tests/rules/`-only wording lags behind the hard-gates checklist. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Tests run:** `_tests/rules/test_rule_cross_references.py` lines 89–119 check that the template, tiers, scorecard README, the three on-demand children and `test_rules_structure.py` all exist.<br>• 🧪 **Agent pointer checked:** `_tests/rules/03_authoring_guidelines/test_authoring_agents.py` line 160 checks the pointer on line 41.<br>• ⚠️ **Gaps:** nothing checks the line 32 `claude_rule_loading_strategy.md` pointer or the two shared-standards children on lines 69 and 71. |
| **Overall** | **7.0/10** | 2026-10-25 | • 💪 **Strength:** a tested, well-split process guide whose children record real mistakes.<br>• ⚠️ **Gap:** style slips in the checklist bullets, and an always-on placement that its narrow `applies_to` doesn't fully support. |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — the rule being scored
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_rules/_common_mistakes.md` — child, scored as part of this rule
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_rules/_hard_gates_checklist.md` — child, scored as part of this rule
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage dimension
