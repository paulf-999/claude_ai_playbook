# Quality Scorecard — test_authoring_skills.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-17

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (SKILL.md structure, contract and triggers) + Scope 1 (`_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** the guide every new skill is written from |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 9 test functions and 16 assertions<br>• 🧩 **Checks:** section order, the frontmatter example's own name and maturity, contract fields, and the maturity table against the checklist and complexity formula<br>• ✂️ **Trimmed:** the ~60-line wording pin, 2026-10-11 |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header version 5.0.1 updated 2026-10-11 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🐛 **Bug fixed:** the old checks matched words like "use" and "avoid" that any text contains, so they could never fail<br>• 🛡️ **Cross-check:** the checklist must ask for the same contract fields |
| **Overall** | **9.3/10** | 2026-10-11 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_skills.py` — the test being scored
- `src/claude/rules/03_authoring_guidelines/authoring_skills.md` — the rule it guards, with its on-demand children
- `src/claude/_tests/_helpers/_resolved_rule.py` — inlines the rule's children before checking
