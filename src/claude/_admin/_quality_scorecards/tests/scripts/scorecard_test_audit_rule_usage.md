# Quality Scorecard — test_audit_rule_usage.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring says what the audit counts<br>• 💬 **Fixture:** `make_transcripts` lists what each session does |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 2 (applied, loaded, flags, history) + Scope 0 (one script) + Dependencies 0 + Prerequisites 1 (`tmp_path` rules and transcripts) |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Target:** the audit's numbers decide which rules get promoted, demoted or archived |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 21 test functions and 44 assertions<br>• 🧩 **Covers:** entry points, globs, `applies_to` headers, miss cost, applied, loaded, misses, dates, symlinks, sections, flags, history and argument errors |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current script |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Real formats:** fixtures use the `instructions`, `nested_memory` and `tool_use` records found in real transcripts |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), from covering four concepts |

## 🔗 Related files

- `src/claude/_tests/scripts/test_audit_rule_usage.py` — the test being scored
- `src/claude/_scripts/audit_rule_usage.py` — what the test guards
- `src/claude/_admin/_audits/audit_rule_usage.md` — the report it produces
