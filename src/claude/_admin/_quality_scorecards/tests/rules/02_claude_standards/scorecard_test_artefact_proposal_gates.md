# Quality Scorecard — test_artefact_proposal_gates.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 6.1/10

**Recommended improvements:**
- Complete the metadata header: add `Test complexity score` and `Python style compliant`
- Replace the 7 functions that only re-check their own literal lists with checks against `_artefact_proposal_gates.md`
- Update the comments to the current five tier names

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 95% of assertions carry a failure message |
| **Complexity** | 7/10 | • 🧮 **Complexity:** estimated raw complexity 3 — the header has no complexity score |
| **Evidence of Need** | 6/10 | • 🔗 **Target:** guards a real, installed artefact<br>• ⚠️ **Finding:** 7 of 12 functions only re-check the literal lists they define, so they don't read the rule at all |
| **Coverage** | 5/10 | • 📊 **Counts:** 12 test functions and 21 assertions<br>• ⚠️ **Finding:** only 5 of the 12 functions check the rule itself |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header is missing `Test complexity score` and `Python style compliant` |
| **Currency** | 6/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17<br>• ⚠️ **Finding:** comments still name the retired `01_core`, `02_claude_internal` and `03_lazy_load` tiers |
| **Regression Value** | 4/10 | • 🛡️ **Failure cases:** 3 test functions named for a failure case<br>• ⚠️ **Finding:** those 7 functions would still pass if the rule file were deleted |
| **Overall** | **6.1/10** | • 💪 **Strongest:** Clarity (9/10)<br>• ⚠️ **Weakest:** Regression Value (4/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_artefact_proposal_gates.py` — the test being scored
- `src/claude/_rules/02_claude_standards/behaviour/_artefact_proposal_gates.md` — what the test guards
