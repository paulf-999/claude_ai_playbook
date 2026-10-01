# Quality Scorecard — test_enforcement_writing_style.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 7.9/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (5) down to 3 or less
- Fix the style gaps and set `Python style compliant: Yes`
- Rename the hook in the module docstring to `hook_enforcement_writing_style.sh`
- Update fixture paths from the retired `01_core` tier to a current tier name

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 7/10 | • 🔍 **Messages:** every test function has a docstring, and 87% of assertions carry a failure message<br>• ⚠️ **Docstring:** module docstring calls it the `enforcement_markdown_file_locations` hook, an old name |
| **Complexity** | 5/10 | • 🧮 **Complexity:** header complexity score 5/10 (raw complexity 5) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 10/10 | • 📊 **Counts:** 21 test functions and 31 assertions |
| **Structural Compliance** | 7/10 | • ✅ **Header:** header says `Python style compliant: No` |
| **Currency** | 7/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17<br>• ⚠️ **Finding:** fixture paths still use the retired `01_core` tier name |
| **Regression Value** | 10/10 | • 🛡️ **Failure cases:** 8 test functions named for a failure case |
| **Overall** | **7.9/10** | • 💪 **Strongest:** Coverage and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (5/10) |

## 🔗 Related files

- `src/claude/_tests/hooks/enforcement/test_enforcement_writing_style.py` — the test being scored
- `src/claude/hooks/hook_enforcement_writing_style.sh` — what the test guards
