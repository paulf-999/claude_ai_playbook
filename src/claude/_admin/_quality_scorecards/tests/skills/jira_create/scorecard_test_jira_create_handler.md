# Quality Scorecard — test_jira_create_handler.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 7.4/10

**Recommended improvements:**
- Add failure messages that say how to fix each assertion (0% have one today)
- Fix the style gaps and set `Python style compliant: Yes`
- Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 5/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 0% of assertions carry a failure message |
| **Complexity** | 7/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 7/10 (raw complexity 3) |
| **Evidence of Need** | 7/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact<br>• ⚠️ **Finding:** tests a Python handler kept beside the test, while the skill itself runs from its SKILL.md instructions |
| **Coverage** | 10/10 | 2026-09-30 | • 📊 **Counts:** 30 test functions and 67 assertions |
| **Structural Compliance** | 7/10 | 2026-10-01 | • ✅ **Header:** header says `Python style compliant: No` |
| **Currency** | 6/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, but has no header dates to show when it last changed |
| **Regression Value** | 10/10 | 2026-09-30 | • 🛡️ **Failure cases:** 9 test functions named for a failure case |
| **Overall** | **7.4/10** | 2026-10-01 | • 💪 **Strongest:** Coverage and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity (5/10) |

## 🔗 Related files

- `src/claude/_tests/skills/jira_create/test_jira_create_handler.py` — the test being scored
- `src/claude/_tests/skills/jira_create/jira_create_handler.py` — what the test guards
- `src/claude/skills/_atlassian_skills/jira_create/SKILL.md` — what the test guards
