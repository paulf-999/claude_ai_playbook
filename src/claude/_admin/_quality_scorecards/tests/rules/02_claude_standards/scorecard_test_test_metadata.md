# Quality Scorecard — test_test_metadata.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Goal:** module docstring says what drift the test stops<br>• 🔍 **Messages:** every failure lists each file and what to fix |
| **Complexity** | 7/10 | • 🧮 **Complexity:** header complexity score 7/10 (raw complexity 3) — Concepts 2 (header order and values, quality band) + Scope 1 (`_tests/`) |
| **Evidence of Need** | 9/10 | • 🔗 **Incident:** the 2026-10-01 baseline found 19 drifting headers, fixed by hand in `release/complete_test_metadata_headers` |
| **Coverage** | 10/10 | • 📊 **Counts:** 19 test functions and 28 assertions<br>• 🧩 **Edge cases:** missing title, missing field, wrong and old order, bad values, `[placeholder]`, banners, dates, class methods and the band edges |
| **Structural Compliance** | 10/10 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | • 🔍 **References:** the fields and bands match `_test_metadata.md` as of 2026-10-01 |
| **Regression Value** | 10/10 | • 🛡️ **Mutation check:** setting `test_git.py` to 10/10 fails the guard<br>• 🧪 **Self-tests:** each check is proven against a synthetic bad header |
| **Overall** | **9.3/10** | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), at the floor for new tests |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_test_metadata.py` — the test being scored
- `src/claude/_rules/02_claude_standards/testing/_test_metadata.md` — the standard the test guards
