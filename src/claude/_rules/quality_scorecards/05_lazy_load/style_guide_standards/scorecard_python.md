# Quality Scorecard — python.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.8/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a dedicated structural test for this file.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 📋 **Concrete:** a worked reST docstring example, an explicit PEP 8 override (120 chars, ruff-enforced), specific comment-placement rules |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** 10 distinct sections (layout, naming, imports, strings, errors, docstrings, functions, type hints, comments, general), single file, no dependencies |
| **Evidence of Need** | 8/10 | • 🔗 **Concrete tooling tie-in:** the 120-character override is specific and `ruff`-enforced, not generic style advice |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | • ✅ **Fixed:** "## 🔗 Related" now has its emoji, matching every other heading in the file<br>• ✅ **Otherwise compliant:** Purpose statement, Contents section, well within line limit |
| **Currency** | 9/10 | • ✅ **Fixed:** the `[[python_environment]]` wiki-link is now a real markdown link<br>• ✅ **Fixed:** the parent now links all 4 genuine sibling pages (`testing.md`, `logging.md`, `module_organisation.md`, `code_complexity.md`)<br>• ✅ **Fixed:** both orphaned duplicates removed — `python/python.md`, and `python/python_standards.md` (found during this same cleanup; not merely an unreferenced sibling as first assessed, but a second near-identical copy of this parent) |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **6.8/10** | • 💪 **Strength:** concrete, tooling-backed conventions, now fully connected to its real children with no orphans left<br>• ⚠️ **Gap:** zero test coverage remains the only open item |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/python.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/python_environment.md` — Currency dimension
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/testing.md` — Currency dimension
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/logging.md` — Currency dimension
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/module_organisation.md` — Currency dimension
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/code_complexity.md` — Currency dimension

---

## 🚩 Pre-existing issues — found here, fixed separately

- 🐛 **Broken link syntax:** "Related" used `[[python_environment]]` — the memory system's wiki-link format, not a resolvable reference in a `_rules/` file.
- 🐛 **Domain disconnect:** unlike `airflow.md`/`dbt.md`, this parent had no links to `testing.md`, `logging.md`, `module_organisation.md`, or `code_complexity.md`.
- 🐛 **Two orphaned duplicates, not one:** `python/python.md` was an unreferenced near-copy of this parent — and so, it turned out on closer inspection, was `python/python_standards.md` (initially misclassified as a genuine sibling page rather than a second duplicate).
- ✅ **Disposition:** all four fixed directly in this same audit pass, per explicit request — not left open.
