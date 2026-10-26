# Quality Scorecard — claude_usage_standards.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.6/10

**Recommended improvements:**
- Replace line 11's import-era reason with the file's current job, the directory-structure pointer
- Use one path base for the Contents "see" paths on lines 17–19
- Split line 11 into one-sentence bullets and give the Contents bullets bold keywords

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear index:** each of the three `##` sections holds one pointer line, and each says how it loads.<br>• ⚠️ **Mixed path bases:** in `rules/01_essentials/claude_usage_standards.md` line 17 the "see" path is relative to `rules/` (`02_claude_standards/...`), but lines 18–19 are relative to `01_essentials/` (`claude_usage_standards/...`), so a reader has to work out the base each time. |
| **Complexity** | 7/10 | 2026-10-25 | • 🧮 **Raw complexity 3:** Concepts 1 (three conventions) + Scope 2 (points into `01_essentials/claude_usage_standards/` and `02_claude_standards/path_scoped_rules/`) + Dependencies 0 + Prerequisites 0 — see `_complexity_scoring.md`.<br>• ⚠️ **Cross-tier pointer:** line 25 reaches into a different tier, which is what lifts Scope above one folder. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ⚠️ **Undated, outdated reason:** line 11 says the file exists because the three conventions were "unreachable from `CLAUDE.md` — no file imported them". It gives no date or issue, and the problem no longer applies, because the children now load on their own (lines 29 and 33).<br>• 🔗 **Real current job:** the only working reason left is the line 25 pointer for new config files, and that reason is recorded only in a test docstring (`_tests/rules/02_claude_standards/test_always_on_reachability.py` line 144), not in an incident. |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • 🎯 **Small and declared:** 34 lines, with `applies_to: *` and `miss_cost: low` on lines 4–5, which the loading strategy allows ("always-on only if small").<br>• ⚠️ **Mostly redundant:** lines 27–33 point to children that load on their own anyway, so only the line 25 pointer earns the always-on cost. |
| **Structural Compliance** | 8/10 | 2026-10-25 | • ✅ **Header and shape:** the version/created/updated header and the three usage fields are on lines 1–6, the H1 has an emoji, the Purpose line is on line 9, the file is 34 lines long, and every child is named in a `Loads on its own from:` or `Read on demand:` line.<br>• ⚠️ **Style slips:** line 11 puts two sentences in one bold-keyword paragraph, and the Contents bullets on lines 17–19 don't open with a bold keyword.<br>• 🔍 **Contents just qualifies:** there are exactly 3 real `##` headings (lines 23, 27, 31), which meets the "3 or more" gate in `_hard_gates_checklist.md` line 23. |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Paths exist:** `claude_directory_structure.md`, `naming_standards.md` and `writing_style.md` are all at the paths named on lines 25, 29 and 33.<br>• ⚠️ **Out-of-date framing:** line 11 describes the old `@import` mechanism ("no file imported them … This parent restores that"). That no longer matches how `rules/` loads, and it breaks `writing_style.md` line 34 ("History lives in git"). |
| **Test Coverage** | 9/10 | 2026-10-25 | • 🧪 **Pointer guarded:** `test_always_on_reachability.py` lines 143–150 fail if the line 25 pointer disappears, and also check that the naming hook backstop still exists.<br>• 🧪 **Layout guarded:** `_tests/rules/01_essentials/test_rule_directory_organisation.py` lines 94–117 pin this file and its child folder, and no incident record needs a content-regression test. |
| **Overall** | **7.6/10** | 2026-10-25 | • 💪 **Small, tested pointer hub:** short, fully wired, and its one working pointer is guarded by a test.<br>• ⚠️ **Out-of-date reason:** line 11's import-era justification is both the Evidence gap and the Currency gap, so cutting it or restating the current need would lift both. |

## 🔗 Related files

- `src/claude/rules/01_essentials/claude_usage_standards.md` — the rule being scored
- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — Test Coverage dimension
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage dimension
