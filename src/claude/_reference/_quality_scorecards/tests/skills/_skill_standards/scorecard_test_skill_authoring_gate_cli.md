# Quality Scorecard — test_skill_authoring_gate_cli.py

**Date Created:** 2026-10-17
**Date Updated:** 2026-10-17

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-10-17 | • 🔍 **Messages:** every test function has a docstring, and every assertion shows the exit code or output it got |
| **Complexity** | 8/10 | 2026-10-17 | • 🧮 **Raw complexity 2:** Concepts 1 (the command line's exit codes and summary) + Scope 0 (fake skills only) + Dependencies 0 + Prerequisites 1 (`tmp_path`, `capsys`, `monkeypatch`) |
| **Evidence of Need** | 9/10 | 2026-10-17 | • 🔗 **Gap:** the linter's `main()` was its largest untested block, 61 of the 140 lines CI coverage missed on 2026-10-17 |
| **Coverage** | 9/10 | 2026-10-17 | • 📊 **Counts:** 5 test functions and 13 assertions<br>• 🧩 **Paths:** missing folder, no skills, clean, warnings only and failures |
| **Structural Compliance** | 10/10 | 2026-10-17 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-17 | • 🔍 **References:** matches the gate linter's `main()` as of 2026-10-17 |
| **Regression Value** | 10/10 | 2026-10-17 | • 🛡️ **Exit codes:** fails if a failing skill stops exiting 1, which would let pre-commit pass a broken skill |
| **Overall** | **9.4/10** | 2026-10-17 | • 💪 **Strongest:** Clarity, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/skills/_skill_standards/test_skill_authoring_gate_cli.py` — the test being scored
- `src/claude/scripts/_lint_scripts/lint_skill_authoring_gate.py` — the gate linter whose command line it proves
- `src/claude/_tests/_helpers/_gate_fixtures.py` — builds the fake skills
