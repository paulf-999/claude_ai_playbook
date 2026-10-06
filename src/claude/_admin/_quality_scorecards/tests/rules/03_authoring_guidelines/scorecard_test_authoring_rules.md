# Quality Scorecard — test_authoring_rules.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (the guide and the files it points to) + Scope 2 (`_rules/`, `_templates/`, `_admin/` and `_tests/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** the guide every new rule is written from |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 11 test functions and 19 assertions<br>• 🧩 **Checks:** checklist, creation steps, tiers, template, scorecard README, on-demand children and gates |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Pointers:** fails if the guide sends authors to a file that was moved or deleted |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_rules.py` — the test being scored
- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — what the test guards
