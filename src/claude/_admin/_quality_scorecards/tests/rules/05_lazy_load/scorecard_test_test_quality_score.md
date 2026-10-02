# Quality Scorecard — test_test_quality_score.py

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-02 | • 🔍 **Goal:** module docstring says what drift the test stops and where the header checks live<br>• 🔍 **Messages:** every failure names the file, its score and the band its counts support |
| **Complexity** | 8/10 | 2026-10-02 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) — Concepts 0 (the quality band) + Scope 2 (`src/claude/_tests/` and `src/sh/claude/_tests/`) |
| **Evidence of Need** | 9/10 | 2026-10-02 | • 🔗 **Incident:** the 2026-10-01 baseline found 19 drifting headers; split out of `test_test_metadata.py` on 2026-10-02 so both stay under the complexity minimum |
| **Coverage** | 9/10 | 2026-10-02 | • 📊 **Counts:** 11 test functions and 17 assertions<br>• 🧩 **Edge cases:** band table and lower-count rule, inflated, deflated and one-past-the-allowance scores, async and class-method tests, malformed and missing score lines |
| **Structural Compliance** | 10/10 | 2026-10-02 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-02 | • 🔍 **References:** the bands match `_test_metadata.md` as of 2026-10-02 |
| **Regression Value** | 10/10 | 2026-10-02 | • 🛡️ **Mutation check:** setting `test_git.py` to 10/10 fails the guard<br>• 🧪 **Self-tests:** each band edge is proven against a synthetic header |
| **Overall** | **9.3/10** | 2026-10-02 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_test_quality_score.py` — the test being scored
- `src/claude/_tests/rules/05_lazy_load/test_test_metadata.py` — the header helpers it reuses
- `src/claude/_rules/05_lazy_load/testing/_test_metadata.md` — the quality table the test guards
