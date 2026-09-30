# Quality Scorecard — test_artefact_proposal_gates.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.9/10

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 7/10 | • 🧮 **Complexity:** header complexity score 7/10 (raw complexity 3) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | • 📊 **Counts:** 17 test functions and 30 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 10/10 | • 🛡️ **Failure cases:** 2 test functions named for a failure case<br>• ✅ **Mutation check:** a mutation check on a broken copy of the rule failed 3 of 3 deliberate breaks, where the previous version passed all 12 of its functions |
| **Overall** | **8.9/10** | • 💪 **Strongest:** Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_artefact_proposal_gates.py` — the test being scored
- `src/claude/_rules/02_claude_standards/behaviour/_artefact_proposal_gates.md` — what the test guards
