# Quality Scorecard — claude_usage_standards.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.3/10

**Recommended improvements:**
- Add a pointer to `claude_usage_standards/multifile_document_organisation.md`, or say plainly why it is reached through `writing_style.md` only.
- Update the Purpose and "Why this file exists" lines so they stop saying "three conventions".
- Rewrite "Why this file exists" as the current reason the file exists, in bold-keyword bullets of one sentence each, and leave the import history to git.
- Record the reachability gap as a dated incident or an issue number.
- Add a test that every rule in `claude_usage_standards/` is named by the parent.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear index:** each section is one pointer that says when to read or where it loads from<br>• ⚠️ **Undercount:** line 9 says "directory structure, naming, and writing style" and line 11 says "these three conventions", but the folder holds a fourth rule, `multifile_document_organisation.md`, that this file never names |
| **Complexity** | 7/10 | 2026-10-25 | • 🧮 **Raw complexity 3:** Concepts 1 (three pointers) + Scope 2 (`rules/01_essentials/claude_usage_standards/` and `rules/02_claude_standards/path_scoped_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ⚠️ **Undated claim:** line 11 says the conventions "were never actually loaded in a live session", but there is no date, issue or session record<br>• 🔗 **Indirect support:** `test_directory_structure_keeps_a_pointer_and_a_backstop` shows the directory-structure pointer is relied on, but no file records repeat use |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • ✅ **Small and scoped:** about 33 lines, with `applies_to: *` and a `loading:` reason set on lines 4–6<br>• ⚠️ **Thin own payload:** the naming and writing-style children load natively anyway, so only the directory-structure pointer (line 25) is unique always-on content |
| **Structural Compliance** | 7/10 | 2026-10-27 | • ✅ **Header and shape:** metadata header, emoji H1 and section headings, Purpose line, and a Contents section earned by 3 `##` headings<br>• ⚠️ **Style slips:** line 11 is a two-sentence paragraph with no bullet<br>• ⚠️ **History in file:** line 11 also tells history ("previously unreachable… This parent restores that"), against `writing_style.md`'s "History lives in git" rule |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Paths exist:** `claude_directory_structure.md`, `naming_standards.md` and `writing_style.md` all exist at the paths named<br>• ⚠️ **Drifted rationale:** line 11 explains the file through imports ("no file imported them"), but its own pointers now say the children load natively<br>• ⚠️ **Stale count:** "three conventions" no longer matches the four rules that `test_rule_directory_organisation.py` expects in the folder |
| **Test Coverage** | 8/10 | 2026-10-27 | • ✅ **Pointer pinned:** `test_always_on_reachability.py` fails if the directory-structure pointer is removed<br>• ✅ **Folder pinned:** `test_rule_directory_organisation.py` pins the top-level files and the child folder<br>• ⚠️ **Gap uncaught:** no test checks that the parent names every child rule, so the missing `multifile_document_organisation.md` pointer passes |
| **Overall** | **7.3/10** | 2026-10-27 | • 💪 **Lean, tested index:** short, every path is real, and the one pointer that matters most is under test<br>• ⚠️ **Drift:** the stated purpose and rationale lag behind the folder's four rules and native loading |

## 🔗 Related files

- `src/claude/rules/01_essentials/claude_usage_standards.md` — the rule being scored
- `src/claude/rules/01_essentials/claude_usage_standards/multifile_document_organisation.md` — Clarity, Currency and Test Coverage (the child the parent doesn't name)
- `src/claude/rules/01_essentials/claude_usage_standards/naming_standards.md` — Currency
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance ("History lives in git") and Currency
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_directory_structure.md` — Currency and Token Cost
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Evidence of Need and Test Coverage
- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — Currency and Test Coverage
