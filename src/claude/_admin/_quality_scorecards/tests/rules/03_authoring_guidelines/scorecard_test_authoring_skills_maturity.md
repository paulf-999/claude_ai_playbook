# Quality Scorecard — test_authoring_skills_maturity.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (maturity, scope and maintenance) + Scope 1 (`_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2000-01-01 | • 🔗 **Target:** maturity decides how many evals and how much complexity a skill may carry |
| **Coverage** | 10/10 | 2000-01-01 | • 📊 **Counts:** 11 test functions and 20 assertions<br>• 🧩 **Checks:** the maturity table, both anti-patterns and all five low-maintenance principles |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Mutation check:** changing the checklist's Tactical eval count to 9–12 fails the sync test<br>• 🛡️ **Cross-check:** complexity caps must match the shared formula |
| **Overall** | **9.4/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_skills_maturity.py` — the test being scored
- `src/claude/_rules/03_authoring_guidelines/authoring_skills.md` — the rule it guards, with its on-demand children
- `src/claude/_rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — the formula its complexity caps must match
