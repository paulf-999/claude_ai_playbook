# Quality Scorecard — test_security_guardrails.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.1/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 6 and 6)
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | • 🧮 **Complexity:** header complexity score 9/10 (raw complexity 1) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 5/10 | • 📊 **Counts:** 6 test functions and 6 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 7/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.1/10** | • 💪 **Strongest:** Clarity, Complexity, Evidence of Need, Structural Compliance and Currency (9/10)<br>• ⚠️ **Weakest:** Coverage (5/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_security_guardrails.py` — the test being scored
- `src/claude/_rules/02_claude_standards/security/_security_guardrails.md` — what the test guards
