# Quality Scorecard — test_plan_mode_phase_gates.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-11

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 10/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 10/10 (raw complexity 0) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 11 test functions and 20 assertions<br>• ✂️ **Trimmed:** structure checks and pins on the parent and plan-format files, which record no incident |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 8/10 | 2026-09-30 | • 🛡️ **Failure cases:** 1 test function named for a failure case |
| **Overall** | **9.0/10** | 2026-10-11 | • 💪 **Strongest:** Complexity (10/10)<br>• ⚠️ **Weakest:** Regression Value (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_plan_mode_phase_gates.py` — the test being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans/_plan_mode_phase_gates.md` — what the test guards
