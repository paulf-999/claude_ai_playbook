# Quality Scorecard — test_skill_domains.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 7/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 7/10 (raw complexity 3) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 10/10 | 2026-09-30 | • 📊 **Counts:** 14 test functions and 16 assertions |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 10/10 | 2026-09-30 | • 🛡️ **Failure cases:** 5 test functions named for a failure case<br>• ✅ **Mutation check:** a mutation check that moved jira back to `_jira_skills` in a copy of the config failed both folder checks |
| **Overall** | **9.0/10** | 2026-09-30 | • 💪 **Strongest:** Coverage (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/03_authoring_guidelines/test_skill_domains.py` — the test being scored
- `src/claude/rules/03_authoring_guidelines/authoring_skills/skill_domains.yaml` — what the test guards
- `src/claude/skills/` — what the test guards
