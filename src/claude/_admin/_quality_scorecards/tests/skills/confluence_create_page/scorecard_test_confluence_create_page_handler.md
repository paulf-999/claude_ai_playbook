# Quality Scorecard — test_confluence_create_page_handler.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 7.7/10

**Recommended improvements:**
- Add failure messages that say how to fix each assertion (1% have one today)
- Split the test by concept to bring raw complexity (6) down to 3 or less
- Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 5/10 | • 🔍 **Messages:** every test function has a docstring, and 1% of assertions carry a failure message |
| **Complexity** | 4/10 | • 🧮 **Complexity:** header complexity score 4/10 (raw complexity 6) |
| **Evidence of Need** | 7/10 | • 🔗 **Target:** guards a real, installed artefact<br>• ⚠️ **Finding:** tests a Python handler kept beside the test, while the skill itself runs from its SKILL.md instructions |
| **Coverage** | 10/10 | • 📊 **Counts:** 40 test functions and 70 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-19 |
| **Regression Value** | 10/10 | • 🛡️ **Failure cases:** 10 test functions named for a failure case |
| **Overall** | **7.7/10** | • 💪 **Strongest:** Coverage (10/10)<br>• ⚠️ **Weakest:** Complexity (4/10) |

## 🔗 Related files

- `src/claude/_tests/skills/confluence_create_page/test_confluence_create_page_handler.py` — the test being scored
- `src/claude/_tests/skills/confluence_create_page/confluence_create_page_handler.py` — what the test guards
- `src/claude/skills/_atlassian_skills/confluence_create_page/SKILL.md` — what the test guards
