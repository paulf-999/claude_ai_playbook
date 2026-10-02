# Quality Scorecard — test_test_score_floor.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-02

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring states the minimum and that no exemptions remain<br>• 🔍 **Messages:** every failure names the file and the score that fell short |
| **Complexity** | 7/10 | 2026-10-02 | • 🧮 **Raw complexity 3:** Concepts 1 (the minimum and its match with the rule) + Scope 2 (`src/claude/_tests/` and `src/sh/claude/_tests/`, plus the one rule file it checks) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Gap closed:** `_test_metadata.md` set the minimum, but 26 of 45 tests missed it with nothing failing |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 11 test functions and 15 assertions<br>• 🧩 **Checks:** each missed minimum, missing scores, the scan's reach, and the rule's own numbers |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** matches `_test_metadata.md` 2.0.0, with the `BASELINE` list retired on 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Rule sync:** fails if the rule's 9 and 7 change without this test, or if an exemption list comes back |
| **Overall** | **9.1/10** | 2026-10-02 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), at the floor for new tests |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_test_score_floor.py` — the test being scored
- `src/claude/_tests/rules/05_lazy_load/test_test_metadata.py` — the header helpers it reuses
- `src/claude/_rules/05_lazy_load/testing/_test_metadata.md` — the standard the test enforces
