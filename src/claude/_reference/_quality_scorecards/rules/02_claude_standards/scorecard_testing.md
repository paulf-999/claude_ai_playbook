# Quality Scorecard — testing.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Fix the relative links on lines 74–78, which point to a folder that doesn't exist
- Replace line 48's `test_aliases_behavior.py`, which isn't in the repo
- Extend `test_testing.py` to check link targets, not just the backticked path
- Swap the ML examples on lines 39–41 for config-test examples, and use British "behaviour"

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear core:** the line 17 rule of thumb and the lines 21–31 list make clear when a test is needed.<br>• ⚠️ **Off-domain goals:** `testing.md` lines 39–41 use ML examples ("sentiment classification", F1, accuracy) that don't fit the config tests this rule governs.<br>• ⚠️ **Child conflict:** `_test_metadata_audit.md` line 53 says complexity "caps the achievable quality score", but `_test_metadata.md` line 15 calls them "independent minimums".<br>• ⚠️ **Run recipe drift:** `_test_metadata_audit.md` line 18 says `pytest ~/.claude/_tests/`, which differs from the parent's lines 85–86 recipe. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 2 (five sections: when required, goals, layers, writing, running) + Scope 2 (spans `rules/` and `_tests/`) + Dependencies 1 (pytest) + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Broad reach:** the five on-demand children (lines 74–78), plus a grandchild `_test_metadata_complexity_scoring.md` reached through `_test_metadata.md` line 76, widen the surface. |
| **Evidence of Need** | 7/10 | 2026-10-25 | • 🔗 **Dated in children:** `_testing_anti_patterns.md` line 102 (37 wording-pinning tests deleted 2026-10-11) and `_test_metadata.md` line 59 (count padding, 2026-10-11).<br>• ⚠️ **None for the core rule:** `testing.md` lines 15–31 record no incident or usage for "every new code artifact needs a test", and line 29 cites another rule's incident only as an example. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — path-scoped rule in `path_scoped_rules/`, so the rubric leaves this out of the average<br>• 🔍 **Reviewer note:** the lines 1–7 `paths:` frontmatter loads it only for `*.py`, `*.sh`, `*.sql` and `_tests/**`, which the reviewer would have scored 9/10. |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Basics met:** metadata header on lines 8–10 after the frontmatter, emoji H1 on line 13, Purpose on line 15, 90 lines and no Related section.<br>• ⚠️ **Spelling mix:** American "behavior" on lines 15, 37 and 48 sits beside British "behaviour" on line 25, against `writing_style.md`.<br>• ⚠️ **Broken links:** the relative targets `../_rules_lazy_load/testing_lazy_load/...` on lines 74–78 resolve to `rules/02_claude_standards/_rules_lazy_load/`, which doesn't exist (the files are in `rules/_rules_lazy_load/testing_lazy_load/`). |
| **Currency** | 6/10 | 2026-10-25 | • 🔍 **Mostly current:** every test file named in the line 62–68 table exists under `_tests/`, and so do `_shared_paths.py` and `_tests/README.md`.<br>• ⚠️ **Missing file:** line 48 names `test_aliases_behavior.py`, which isn't anywhere in the repo.<br>• ⚠️ **Dead targets:** the same five relative link targets on lines 74–78 point at a folder that isn't there. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Runs:** `_tests/rules/02_claude_standards/test_testing.py` lines 164–169 check that every "Read on demand" pointer resolves, and lines 77–135 enforce the hook-to-test mapping.<br>• ✅ **No incident test needed:** the rule records no incident of its own, so no content-regression test is due.<br>• ⚠️ **Gap:** the line 166 regex reads only the backticked `~/` path, so the broken relative targets (lines 74–78) and the missing `test_aliases_behavior.py` (line 48) pass unnoticed. |
| **Overall** | **6.7/10** | 2026-10-25 | • 💪 **Strengths:** path-scoped loading, a lean 90-line parent and a pointer-existence test that actually runs.<br>• ⚠️ **Gaps:** two stale references (line 48 and lines 74–78), contradictory child guidance and no recorded evidence for the core rule. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/path_scoped_rules/testing.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_testing.py` — Test Coverage dimension

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Broken anchor:** the Contents section (line 9) links to `#-child-files-load-as-needed`, but no `##` heading in the file reads "Child Files (Load As Needed)" — confirmed via `grep "^## " testing.md`, which lists no such heading.
- 🚫 **Effect:** the link 404s within the rendered doc; a reader following Contents to find "child files" lands nowhere.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
