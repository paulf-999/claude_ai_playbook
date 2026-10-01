# Quality Scorecard — test_writing_style.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.3/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 7 and 14)
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 9/10 (raw complexity 1) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 6/10 | 2026-09-30 | • 📊 **Counts:** 7 test functions and 14 assertions |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 7/10 | 2026-09-30 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.3/10** | 2026-10-01 | • 💪 **Strongest:** Clarity, Complexity, Evidence of Need, Structural Compliance and Currency (9/10)<br>• ⚠️ **Weakest:** Coverage (6/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_writing_style.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — what the test guards
