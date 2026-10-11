# Quality Scorecard — test_no_wording_pinning.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-10-11 | • 🔍 **Goal:** module docstring says what is flagged, what passes and how to tag a kept check<br>• 💬 **Messages:** each failure lists the file, test, line and phrase, and the three ways to fix it |
| **Complexity** | 8/10 | 2026-10-11 | • 🧮 **Raw complexity 2:** Concepts 1 (wording pins and finished-migration checks, with tag exemptions) + Scope 1 (`_tests/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2026-10-11 | • 🔗 **Incident:** 37 wording-pinning and migration tests were deleted on 2026-10-11, after breaking on rewording without catching a bug |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 7 test functions and 17 assertions<br>• 🧩 **Cases:** `in`, `not in`, `re.search` and loop phrases, tags with and without a reason, single tokens, regex, `tmp_path` and absent-path checks |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 1.1.0 updated 2026-10-11 |
| **Regression Value** | 9/10 | 2026-10-11 | • 🎯 **Recall:** flags 30 of the 37 deleted tests in the pre-deletion backup<br>• ⚠️ **Misses:** 7 structural or single-word checks the heuristic can't tell from real ones |
| **Overall** | **9.4/10** | 2026-10-11 | • 💪 **Strongest:** Clarity, Evidence of Need, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_no_wording_pinning.py` — the test being scored
- `src/claude/rules/_rules_lazy_load/testing_lazy_load/_testing_anti_patterns.md` — the Wording-Pinning Test anti-pattern it enforces
- `src/claude/rules/02_claude_standards/path_scoped_rules/testing.md` — the incident-records-only content-regression rule
