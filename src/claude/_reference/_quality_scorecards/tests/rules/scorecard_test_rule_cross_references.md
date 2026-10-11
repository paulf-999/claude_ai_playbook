# Quality Scorecard — test_rule_cross_references.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-11 | • 🔍 **Messages:** every test has a docstring, and every assertion names the pointer or fact that broke<br>• 🗂️ **Layout:** one labelled section per rule |
| **Complexity** | 7/10 | 2026-10-11 | • 🧮 **Raw complexity 3:** Concepts 1 (pointers resolve, and repeated facts agree) + Scope 2 (`rules/`, `skills/`, `hooks/`, `agents/` and `settings.json`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 8/10 | 2026-10-11 | • 🔗 **Target:** rules were moved repeatedly during the v2 reset, which is when a pointer silently breaks<br>• 🧩 **Origin:** merged from seven per-rule files whose phrase pins were dropped on 2026-10-11 |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 22 test functions and 38 assertions<br>• 🧩 **Rules:** writing_style, _security_guardrails, authoring_rules, _artefact_proposal_gates, claude_operational_efficiency and git<br>• ✂️ **Trimmed:** the 2 _decision_making pins and a finished-migration check, 2026-10-11 |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 2.0.1 updated 2026-10-11 |
| **Regression Value** | 9/10 | 2026-10-11 | • 🛡️ **Self-tests:** synthetic cases prove the gate and Reference parsers return nothing on a broken rule<br>• 🛡️ **Non-vacuous:** the wildcard and child-pointer checks fail on an empty list |
| **Overall** | **8.9/10** | 2026-10-11 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/test_rule_cross_references.py` — the test being scored
- `src/claude/rules/_rules_lazy_load/testing_lazy_load/_test_metadata.md` — the quality and complexity minimums it meets
