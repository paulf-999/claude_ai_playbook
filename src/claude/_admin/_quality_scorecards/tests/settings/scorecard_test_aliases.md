# Quality Scorecard — test_aliases.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.6/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 9/10 | 2026-09-30 | • 🧮 **Raw complexity 1:** Concepts 1 (the alias table and its parser) + Scope 0 (one file) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards `aliases.md`, which is imported into every session |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 17 test functions and 20 assertions<br>• 🧩 **Merged:** core aliases, a Ready alias, Testing exit docs and plan mode, from the old `test_aliases_behavior.py` |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff`<br>• 📁 **Location:** the only aliases test now, since `rules/test_aliases_behavior.py` was merged in |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Failure cases:** a missing table, a wrong header and a short row each fail<br>• 🐛 **Fix:** the old exit-criteria check only printed, and now it asserts |
| **Overall** | **9.6/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity, Complexity and Evidence of Need (9/10) |

## 🔗 Related files

- `src/claude/_tests/settings/test_aliases.py` — the test being scored
- `src/claude/aliases.md` — what the test guards
- `src/claude/_tests/rules/test_aliases_behavior.py` — the sibling test that checks alias behaviour
- `src/claude/_tests/rules/test_aliases_behavior.py` — merged into this test on 2026-10-01 and deleted
