# Quality Scorecard — test_capture_session_prompts.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.1/10

**Recommended improvements:**
- Add failure messages that say how to fix each assertion (14% have one today)
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 14% of assertions carry a failure message |
| **Complexity** | 8/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-09-30 | • 📊 **Counts:** 14 test functions and 36 assertions |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 7/10 | 2026-09-30 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.1/10** | 2026-09-30 | • 💪 **Strongest:** Evidence of Need (9/10)<br>• ⚠️ **Weakest:** Clarity (6/10) |

## 🔗 Related files

- `src/claude/_tests/skills/claude_capture_session_prompts/test_capture_session_prompts.py` — the test being scored
- `src/claude/skills/_claude_skills/claude_capture_session_prompts/capture_session_prompts.py` — what the test guards
