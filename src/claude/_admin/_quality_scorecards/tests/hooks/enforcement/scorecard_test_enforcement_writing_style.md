# Quality Scorecard — test_enforcement_writing_style.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Goal:** module docstring says what the hook checks and why the payload matters<br>• 🔍 **Messages:** every assertion carries a failure message |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** Concepts 2 (root files, reference names, ignored paths, payload handling) + Scope 0 + Dependencies 1 (runs the bash hook) + Prerequisites 0 |
| **Evidence of Need** | 10/10 | • 🔗 **Incident:** the old hook read a path argument Claude Code never passes, so it never fired |
| **Coverage** | 9/10 | • 📊 **Counts:** 14 test functions and 20 assertions<br>• 🧩 **Edge cases:** dated, hyphenated and unprefixed reference files, stray root files, bad payloads, Edit and Write, and manual runs |
| **Structural Compliance** | 10/10 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | • 🔍 **References:** matches `writing_style.md` and the directory rules as of 2026-10-01 |
| **Regression Value** | 10/10 | • 🛡️ **Mutation check:** 7 of the 15 test cases fail against the old hook |
| **Overall** | **9.3/10** | • 💪 **Strongest:** Evidence of Need, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), at the minimum |

## 🔗 Related files

- `src/claude/_tests/hooks/enforcement/test_enforcement_writing_style.py` — the test being scored
- `src/claude/hooks/hook_enforcement_writing_style.sh` — what the test guards
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — the conventions the hook enforces
