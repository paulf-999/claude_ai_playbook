# Quality Scorecard — test_automation_controls.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.6/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 8/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-09-30 | • 📊 **Counts:** 10 test functions and 20 assertions |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 7/10 | 2026-09-30 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.6/10** | 2026-10-01 | • 💪 **Strongest:** Clarity, Evidence of Need, Coverage, Structural Compliance and Currency (9/10)<br>• ⚠️ **Weakest:** Regression Value (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_automation_controls.py` — the test being scored
- `src/claude/rules/_rules_lazy_load/automation_controls.md` — what the test guards
