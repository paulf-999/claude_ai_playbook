# Quality Scorecard — test_jira_create_handler.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 6.9/10

**Recommended improvements:**
- Add failure messages that say how to fix each assertion (0% have one today)
- Add the seven-line metadata header from `_test_metadata.md`
- Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 5/10 | • 🔍 **Messages:** every test function has a docstring, and 0% of assertions carry a failure message |
| **Complexity** | 7/10 | • 🧮 **Complexity:** estimated raw complexity 3 — the header has no complexity score |
| **Evidence of Need** | 7/10 | • 🔗 **Target:** guards a real, installed artefact<br>• ⚠️ **Finding:** tests a Python handler kept beside the test, while the skill itself runs from its SKILL.md instructions |
| **Coverage** | 10/10 | • 📊 **Counts:** 30 test functions and 67 assertions |
| **Structural Compliance** | 3/10 | • ✅ **Header:** no metadata header |
| **Currency** | 6/10 | • 🔍 **References:** passes against the current config, but has no header dates to show when it last changed |
| **Regression Value** | 10/10 | • 🛡️ **Failure cases:** 9 test functions named for a failure case |
| **Overall** | **6.9/10** | • 💪 **Strongest:** Coverage (10/10)<br>• ⚠️ **Weakest:** Structural Compliance (3/10) |

## 🔗 Related files

- `src/claude/_tests/skills/jira_create/test_jira_create_handler.py` — the test being scored
- `src/claude/_tests/skills/jira_create/jira_create_handler.py` — what the test guards
- `src/claude/skills/_atlassian_skills/jira_create/SKILL.md` — what the test guards
