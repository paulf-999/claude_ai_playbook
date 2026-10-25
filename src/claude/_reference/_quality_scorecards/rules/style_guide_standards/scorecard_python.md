# Quality Scorecard — python.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Move "Meaningful names" and "No history in names" (lines 35–36) out from under "Constants"
- Give the 6 children `_` prefixes, and add a Purpose line to `python/python_environment.md`
- Record evidence of need, and add an exception for top-level handlers to the `except` rule on line 50

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Mostly direct:** layout, naming, imports and docstring rules are short and testable, and the two docstring examples (python.md lines 57–72) make the default plain.<br>• ⚠️ **Misplaced nesting:** "Meaningful names" and "No history in names" sit as child bullets under "Constants" (python.md lines 35–36), but they apply to every identifier.<br>• ⚠️ **Subjective trigger:** "Add type hints when they add value" (python.md line 88) leaves the call to each reader.<br>• ⚠️ **No escape hatch:** "never bare `except:` or `except Exception:`" (python.md line 50) has no exception for top-level handlers, so readers will apply it differently. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (10 `##` topic sections plus 6 child pages) + Scope 1 (one style-guide tree, `python.md` plus `python/`) + Dependencies 1 (`ruff`, line 14) + Prerequisites 0.<br>• ⚠️ **Breadth:** the parent covers 10 separate topics (python.md lines 21–100), which is normal for a style guide but far from the raw-1 anchor. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded need:** the Purpose line (python.md line 12) gives a general aim ("consistent, readable … across the team"), with no dated incident, PR or usage record.<br>• 🔗 **Hint only:** "trim long docstrings when a file is next edited" (python.md line 78) suggests a real past decision, but no file records it. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and shape:** has the `paths:` frontmatter, a 3-line metadata header plus `miss_cost`/`loading` (lines 1–9), an H1 emoji, a Purpose line and about 100 counted lines.<br>• ⚠️ **Child naming:** the 6 children (python.md lines 104–109, e.g. `python/comments.md`) have no `_` prefix, so they fail `_hard_gates_checklist.md` line 16.<br>• ⚠️ **Child style slips:** `python/python_environment.md` has no `**Purpose:**` line (lines 4–6), and its bullets have no bold keyword (lines 51–52, 56–58).<br>• ⚠️ **Bullet slip:** "Use f-strings: exclusively; do not use…" (python.md line 46) joins two clauses with a semicolon and is phrased as a negation. |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Links resolve:** all 6 linked children exist on disk under `_reference/_style_guide_standards/python/`.<br>• ⚠️ **Child path drift:** `python/python_environment.md` line 38 points to `python/testing.md` from inside `python/`, and its example path `src/py/airbyte_manager/...` (line 27) refers to a codebase outside this config.<br>• 🔍 **Practice gap:** the "No `:type:` or `:rtype:`" rule (python.md line 76) is not yet followed in the repo's own tests (e.g. `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` lines 74–77), though line 78 allows trimming them later. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Tracked:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 50 checks python.md's header, Purpose line, required H2s, child links, relative links and Contents entries.<br>• 🧪 **Live check:** `_tests/rules/02_claude_standards/test_path_scoped_rules_live.py` line 173 uses python.md as the negative case for `paths:` loading.<br>• ⚠️ **Blind spots:** that test's Contents check only matches `- [` list entries, so the inline `·` Contents on python.md line 18 is never checked.<br>• ⚠️ **Children untracked:** the children are not checked themselves, which is how the missing Purpose in `python_environment.md` goes unnoticed. |
| **Overall** | **6.5/10** | 2026-10-25 | • 💪 **Strength:** concise, testable conventions with good docstring examples and structural test coverage.<br>• ⚠️ **Gaps:** no recorded evidence of need, children named without the `_` prefix, and style slips in `python_environment.md`. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/python.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/python/python_environment.md` — Currency dimension
- `src/claude/_reference/_style_guide_standards/python/testing.md` — Currency dimension
- `src/claude/_reference/_style_guide_standards/python/logging.md` — Currency dimension
- `src/claude/_reference/_style_guide_standards/python/module_organisation.md` — Currency dimension
- `src/claude/_reference/_style_guide_standards/python/code_complexity.md` — Currency dimension

---

## 🚩 Pre-existing issues — found here, fixed separately

- 🐛 **Broken link syntax:** "Related" used `[[python_environment]]` — the memory system's wiki-link format, not a resolvable reference in a `_rules/` file.
- 🐛 **Domain disconnect:** unlike `airflow.md`/`dbt.md`, this parent had no links to `testing.md`, `logging.md`, `module_organisation.md`, or `code_complexity.md`.
- 🐛 **Two orphaned duplicates, not one:** `python/python.md` was an unreferenced near-copy of this parent — and so, it turned out on closer inspection, was `python/python_standards.md` (initially misclassified as a genuine sibling page rather than a second duplicate).
- ✅ **Disposition:** all four fixed directly in this same audit pass, per explicit request — not left open.
