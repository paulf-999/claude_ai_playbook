# Quality Scorecard — test_scorecard_dates.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring states the rule in two sentences<br>• 💬 **Messages:** every assertion carries a failure message, and the real-file scan names the offending scorecard |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (column, ISO date, header ordering) + Scope 1 (one scorecards tree) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Target:** guards the row `Date Updated` rule in the rules, tests and skills scorecard templates |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 16 assertions |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant<br>• 📁 **Location:** only test in the new `_tests/admin/` folder |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against all 87 current scorecards |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Failure cases:** 7 synthetic bad tables, covering the old 3-column header, the separator, non-ISO, impossible and placeholder dates, a row dated after the header and an empty table |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Coverage and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/admin/test_scorecard_dates.py` — the test being scored
- `src/claude/_admin/_quality_scorecards/` — what the test guards
- `src/claude/_admin/_quality_scorecards/rules/README.md` — defines the row `Date Updated` rule
- `src/claude/_admin/_quality_scorecards/tests/README.md` — defines the row `Date Updated` rule
- `src/claude/_templates/skills/_quality_scorecard_template.md` — defines the row `Date Updated` rule
