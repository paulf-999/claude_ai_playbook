# Quality Scorecard — test_test_metadata.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-02

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring says what drift the test stops<br>• 🔍 **Messages:** every failure lists each file and what to fix |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Complexity:** header complexity score 7/10 (raw complexity 3) — Concepts 1 (header order, values and dates) + Scope 2 (`src/claude/_tests/` and `src/sh/claude/_tests/`); quality-score checks moved to `test_test_quality_score.py` |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Incident:** the 2026-10-01 baseline found 19 drifting headers, fixed by hand in `release/complete_test_metadata_headers` |
| **Coverage** | 9/10 | 2026-10-02 | • 📊 **Counts:** 12 test functions and 16 assertions<br>• 🧩 **Edge cases:** missing title, missing field, wrong and old order, bad values, `[placeholder]`, banners and dates |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** the fields and bands match `_test_metadata.md` as of 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Mutation check:** a header-less test dropped into `src/sh/claude/_tests/` fails the scan<br>• 🧪 **Self-tests:** each check is proven against a synthetic bad header |
| **Overall** | **9.1/10** | 2026-10-02 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), at the floor for new tests |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_test_metadata.py` — the test being scored
- `src/claude/_rules_lazy_load/testing/_test_metadata.md` — the standard the test guards
