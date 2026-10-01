# Quality Scorecard — test_skill_authoring_gate.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 7.7/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (5) down to 3 or less
- Fix the style gaps and set `Python style compliant: Yes`
- Turn the manual-review skips into failures, or `xfail` with a tracked reason, so real gaps can't pass quietly

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 5/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 5/10 (raw complexity 5) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-09-30 | • 📊 **Counts:** 10 test functions and 16 assertions |
| **Structural Compliance** | 7/10 | 2026-10-01 | • ✅ **Header:** header says `Python style compliant: No` |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-21 |
| **Regression Value** | 6/10 | 2026-09-30 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case<br>• ⚠️ **Finding:** 9 checks call `pytest.skip` on a real gap, so a failing skill shows as skipped, not failed |
| **Overall** | **7.7/10** | 2026-10-01 | • 💪 **Strongest:** Clarity, Evidence of Need, Coverage and Currency (9/10)<br>• ⚠️ **Weakest:** Complexity (5/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_skill_authoring_gate.py` — the test being scored
- `src/claude/_rules/03_authoring_guidelines/authoring_skills.md` — what the test guards
- `src/claude/skills/` — what the test guards
