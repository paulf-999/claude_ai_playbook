# Quality Scorecard — test_skill_authoring_gate_run.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2000-01-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion shows what the linter reported |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (the run checks and how findings route) + Scope 0 (fake skills only) + Dependencies 0 + Prerequisites 1 (`tmp_path`) |
| **Evidence of Need** | 9/10 | 2000-01-01 | • 🔗 **Target:** keeps blocking failures and advisory warnings in the right place |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 11 test functions and 16 assertions<br>• 🧩 **Checks:** R2–R4 both ways, failures blocking, judgement calls advising, and R1 reported once as C3 |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** matches the gate linter's checks as of 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Routing:** fails if a hard walk check slips to advisory, which would let CI pass a broken skill |
| **Overall** | **9.4/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/skills/test_skill_authoring_gate_run.py` — the test being scored
- `src/sh/claude/skill_authoring_gate_lint.py` — the gate linter whose checks it proves
- `src/claude/_tests/_gate_fixtures.py` — builds the fake skills
