# Quality Scorecard — test_no_orphaned_skill_files.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion says what was flagged |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (orphans, broken links, eager imports) + Scope 2 (`skills/` and `_tests/skills/`) + Dependencies 0 + Prerequisites 0 (in-memory skills, no fixtures) |
| **Evidence of Need** | 10/10 | 2026-10-01 | • 🔗 **Incidents:** found confluence_create_page's dead `templates/` and git_create_pr's three broken links (2026-09-19) |
| **Coverage** | 10/10 | 2026-09-30 | • 📊 **Counts:** 14 test functions and 19 assertions<br>• 🧩 **Edge cases:** self-mentions, external test references, both fence styles and email addresses |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current skills, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-09-30 | • 🛡️ **Pure detectors:** every case is proven on an in-memory skill, with no `tmp_path` or `monkeypatch` |
| **Overall** | **9.4/10** | 2026-10-01 | • 💪 **Strongest:** Evidence of Need, Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/skills/test_no_orphaned_skill_files.py` — the test being scored
- `src/claude/_tests/_skill_orphans.py` — the pure detectors it proves and runs
- `src/claude/_rules_lazy_load/authoring_guidelines/authoring_skills/_no_orphaned_files.md` — the rule it enforces
