# Quality Scorecard — test_audit_claude_component_root.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring says why the root is required<br>• 💬 **Messages:** every assertion carries a failure message |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (how the audit picks its root) + Scope 0 (one script) + Dependencies 0 + Prerequisites 1 (a small `tmp_path` tree) |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Target:** the script lands in the live config too, so a guessed root would scan the wrong folder |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 21 assertions |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Guard:** fails if a default root or repo-guessing constant comes back |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** none below 8/10 |

## 🔗 Related files

- `src/claude/_tests/scripts/test_audit_claude_component_root.py` — the test being scored
- `src/claude/_scripts/_audit_scripts/audit_claude_component.py` — what the test guards
- `src/claude/_rules/02_claude_standards/portable_paths.md` — why the root is never guessed
