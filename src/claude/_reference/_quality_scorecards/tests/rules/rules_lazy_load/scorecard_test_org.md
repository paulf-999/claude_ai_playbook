# Quality Scorecard — test_org.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-11 | • 🔍 **Goal:** module docstring explains the leak rule without naming a term<br>• ⚠️ **Messages:** 8 of 19 assertions carry a failure message |
| **Complexity** | 7/10 | 2026-10-11 | • 🧮 **Raw complexity 3:** Concepts 1 (term leaks and the org index) + Scope 3 (the whole config) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-11 | • 🔗 **Target:** keeps one organisation's names and IDs out of files that are shared |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 14 test functions and 19 assertions<br>• 🧩 **Checks:** term loading, case-insensitive leaks, allowed org pointers, skipped folders, exceptions and the org index |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 1.3.6 updated 2026-10-11 |
| **Regression Value** | 10/10 | 2026-10-11 | • 🛡️ **Failure cases:** a leaked term and an unlisted org rule are both caught on made-up files |
| **Overall** | **8.9/10** | 2026-10-11 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity and Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/rules_lazy_load/test_org.py` — the test being scored
- `src/claude/rules/_rules_lazy_load/org.md` — the organisation index it checks
- `src/claude/rules/_rules_lazy_load/org/` — where the term list lives, when a config has organisation content
