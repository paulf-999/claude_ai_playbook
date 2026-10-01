# Quality Scorecard — test_decision_making.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (the intentionality gate) + Scope 2 (`behaviour/` and `naming_standards/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** the rule that makes Claude present options instead of deciding alone |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 17 assertions<br>• 🧩 **Checks:** 2–3 options, the recommended label, waiting, each exemption and both cross-references |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Cross-checks:** fails if `_naming_principles.md` stops saying 3–4 candidates, so the exception can't go stale |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_decision_making.py` — the test being scored
- `src/claude/_rules/02_claude_standards/behaviour/_decision_making.md` — what the test guards
