# Quality Scorecard — test_skill_instructions_section.py

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-02 | • 🔍 **Messages:** every test function has a docstring, and 42% of assertions carry a failure message |
| **Complexity** | 8/10 | 2026-10-02 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) |
| **Evidence of Need** | 10/10 | 2026-10-02 | • 🔗 **Incident:** on 2026-10-01 Claude skipped the Confluence draft review because its must-follow rules sat in `reference/`, never read |
| **Coverage** | 9/10 | 2026-10-02 | • 📊 **Counts:** 14 test functions and 19 assertions, run against every installed skill |
| **Structural Compliance** | 9/10 | 2026-10-02 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-02 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-02 | • 🛡️ **Failure cases:** synthetic SKILL.md fixtures prove a missing section, a late section, missing rules, a missing reference and a config-folder drafts path are each caught |
| **Overall** | **9.0/10** | 2026-10-02 | • 💪 **Strongest:** Evidence of Need and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity (7/10) |

## 🔗 Related files

- `src/claude/_tests/skills/test_skill_instructions_section.py` — the test being scored
- `src/claude/_rules_lazy_load/authoring_skills/_core_standards.md` — the rule the test enforces
