# Quality Scorecard — test_test_score_floor.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-11

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring states the minimum and that no exemptions remain<br>• 🔍 **Messages:** every failure names the file and the score that fell short |
| **Complexity** | 7/10 | 2026-10-02 | • 🧮 **Raw complexity 3:** Concepts 1 (the minimum and its match with the rule) + Scope 2 (`src/claude/_tests/` and `src/claude/_install/_tests/`, plus the one rule file it checks) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Gap closed:** `_test_metadata.md` set the minimum, but 26 of 45 tests missed it with nothing failing |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 9 test functions and 12 assertions<br>• 🧩 **Checks:** each missed minimum, missing scores and the rule's own numbers<br>• ✂️ **Trimmed:** the no-exemption-list migration check and an enforcer-name pin, 2026-10-11 |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 4.0.0 updated 2026-10-11 |
| **Regression Value** | 10/10 | 2026-10-11 | • 🛡️ **Rule sync:** fails if the rule's quality 7 or complexity 7 changes without this test |
| **Overall** | **9.1/10** | 2026-10-11 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/rules_lazy_load/test_test_score_floor.py` — the test being scored
- `src/claude/_tests/rules/rules_lazy_load/test_test_metadata.py` — the header helpers it reuses
- `src/claude/rules/_rules_lazy_load/testing_lazy_load/_test_metadata.md` — the standard the test enforces
