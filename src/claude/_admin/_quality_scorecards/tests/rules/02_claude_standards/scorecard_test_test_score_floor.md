# Quality Scorecard — test_test_score_floor.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring states the minimum and how `BASELINE` works<br>• 🔍 **Messages:** every failure names the file and the score that broke |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (minimum, ratchet, stale paths) + Scope 1 (`_tests/`) + Dependencies 1 (helpers from `test_test_metadata.py`) + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Gap:** `_test_metadata.md` set the minimum, but 26 of 45 tests missed it with nothing failing |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 15 test functions and 20 assertions<br>• 🧩 **Edge cases:** each missed minimum, every regression, partial improvement, stale entries, missing paths and missing scores |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** the minimums and `BASELINE` match `_test_metadata.md` and the headers as of 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Mutation check:** lowering `test_git.py` from 5/10 to 4/10 fails the scan<br>• 🧪 **New file check:** a new 5/10 test file fails the scan |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), exactly at the minimum |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_test_score_floor.py` — the test being scored
- `src/claude/_tests/rules/02_claude_standards/test_test_metadata.py` — the header helpers it reuses
- `src/claude/_rules/02_claude_standards/testing/_test_metadata.md` — the standard the test enforces
