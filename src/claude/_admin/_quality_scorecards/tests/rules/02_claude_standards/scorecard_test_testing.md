# Quality Scorecard — test_testing.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 7/10 | 2026-09-30 | • 🧮 **Raw complexity 3:** Concepts 1 (hook-to-test mapping and testing.md's pointers) + Scope 2 (`hooks/`, `_tests/hooks/` and `_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** enforces testing.md's own rule that every enforcement hook has a test |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 10 test functions and 16 assertions<br>• 🧩 **New:** aspect-split test names, the word-boundary edge case, testing.md's children and the score-minimum enforcer |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Sanity check:** fails if the hook or test folders come back empty, which used to make the checks pass silently |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_testing.py` — the test being scored
- `src/claude/_rules/02_claude_standards/testing.md` — what the test guards
