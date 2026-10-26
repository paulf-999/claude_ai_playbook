# Quality Scorecard — portable_paths.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.3/10

**Recommended improvements:**
- Correct line 23's "all three shipped", since four incidents follow
- Extend `test_portable_paths_python.py` to scan `scripts/` as well as `_tests/`
- Add a content-regression test for the incident record on lines 21–28
- Split line 38 into one-sentence bullets and use British "recognised" on line 28

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🎯 **Actionable:** the Python and shell instructions give exact replacement code (lines 35, 41), so two readers would apply them the same way<br>• ⚠️ **Count mismatch:** `portable_paths.md` line 23 says "all three shipped", but four incident bullets follow (lines 25–28)<br>• ⚠️ **Scope drift:** the Purpose (line 9) says "hooks and tests", while `applies_to` (line 4) and line 34 also cover `scripts/` |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (CLAUDE_DIR resolution, the `.expanduser()` reservation, import-prefix parsing, shell self-location, guard clauses) + Scope 2 (hooks, `_tests/` and `scripts/`, per line 4) + Dependencies 0 + Prerequisites 0<br>• ⚠️ **Several jobs:** lines 34–42 cover five separate anti-patterns across two languages, which puts it between the raw-3 and raw-5 anchors |
| **Evidence of Need** | 9/10 | 2026-10-25 | • 📈 **Recurring:** four dated incidents over 2026-09-17 and 2026-09-18 (lines 23–28), one of them in this rule's own test, minutes after the rule was written |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • ⚖️ **Narrow but always-on:** `applies_to` (line 4) limits it to hooks, tests and scripts, yet it loads every session<br>• ⚠️ **Defended placement:** line 6 says a new hook or test can start before a matching file is open, and line 5 rates the miss cost high, which makes this arguable but not the ~9 anchor |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Header and length:** a metadata header (lines 1–6), an emoji H1, a one-line Purpose and 45 lines<br>• ⚠️ **Multi-sentence bullet:** line 38 holds three sentences in one bullet<br>• ⚠️ **Keyword form:** lines 37 and 38 bold a whole clause before an em dash, not a `**keyword:**` lead-in<br>• ⚠️ **Spelling:** line 28 uses American "recognized" |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Guidance current:** every path in How to apply exists today (`_tests/_helpers/_shared_paths.py`, `_templates/utils/shell_utils.sh`)<br>• ⚠️ **Missing files:** line 25's `test_response_standards_hook.py` / `_inject.py` and line 27's `hook_enforcement_dir_structure.sh` are not on disk (they are named only in incident history)<br>• ⚠️ **Moved check:** line 26 places the import-reachability check in `test_rules_structure.py`, but the config-dir detection now sits in `test_rules_structure_layout.py` (line 36) |
| **Test Coverage** | 7/10 | 2026-10-25 | • ✅ **Runs:** `test_portable_paths_hooks.py` and `test_portable_paths_python.py` enforce the rule and prove each pattern against real and harmless lines<br>• ⚠️ **No incident regression:** no test pins the incident record's key phrases (lines 21–28), which the hard gates require for rules that record an incident<br>• ⚠️ **Scripts unscanned:** `test_portable_paths_python.py` line 27 scans only `_tests/`, though rule lines 4 and 34 cover `scripts/` too |
| **Overall** | **7.3/10** | 2026-10-25 | • 💪 **Strength:** strong dated evidence, plus enforcement tests that actually run<br>• ⚠️ **Gaps:** style slips (line 38), stale incident file names (lines 25 and 27), no incident content-regression test, and `scripts/` not scanned |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/portable_paths.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_hooks.py` — Test Coverage dimension (hooks)
- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_python.py` — Test Coverage dimension (Python)
