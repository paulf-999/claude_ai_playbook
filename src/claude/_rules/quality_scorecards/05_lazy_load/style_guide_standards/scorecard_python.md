# Quality Scorecard — python.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 5.8/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Fix the "Related" heading: add an emoji (it's the only heading in this file without one), and replace the `[[python_environment]]` wiki-link syntax with a real markdown link to `python/python_environment.md` — the double-bracket syntax doesn't resolve to anything in a rule file.
- Route to (or explain the relationship with) the 5 other detail pages that live in `python/` — `testing.md`, `logging.md`, `module_organisation.md`, `code_complexity.md`, `python_standards.md` — none of which this parent currently mentions.
- Delete or reconcile the orphaned duplicate `python/python.md`.
- Add a dedicated structural test for this file.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 📋 **Concrete:** a worked reST docstring example, an explicit PEP 8 override (120 chars, ruff-enforced), specific comment-placement rules |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** 10 distinct sections (layout, naming, imports, strings, errors, docstrings, functions, type hints, comments, general), single file, no dependencies |
| **Evidence of Need** | 8/10 | • 🔗 **Concrete tooling tie-in:** the 120-character override is specific and `ruff`-enforced, not generic style advice |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | • 🚩 **One heading missing emoji:** "## Related" is the only heading in the file without one, breaking `writing_style.md`'s "use on all major headings" rule<br>• ✅ **Otherwise compliant:** Purpose statement, Contents section, well within line limit |
| **Currency** | 3/10 | • 🐛 **Broken link syntax:** "Related" uses `[[python_environment]]`, a wiki-link syntax with no resolution mechanism in this codebase's rule files (it's the personal-memory system's link format) — and even as prose it omits the real path, `python/python_environment.md`<br>• 🐛 **Disconnected from its own domain:** this parent never references 5 of the 6 files living in `python/` (`testing.md`, `logging.md`, `module_organisation.md`, `code_complexity.md`, `python_standards.md`)<br>• 🐛 **Orphaned duplicate:** `python/python.md` is a near-identical, unreferenced copy of this file |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **5.8/10** | • 💪 **Strength:** concrete, tooling-backed conventions for the content it does cover<br>• ⚠️ **Gap:** the lowest-scoring file in this survey — a broken link, a disconnected domain structure, an orphaned duplicate, and zero tests |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/python.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/python.md` — Currency dimension (the orphaned duplicate)
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/python_environment.md` — Currency dimension (the real target of the broken `[[python_environment]]` link)
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/testing.md` — Currency dimension (an unreferenced sibling in its own domain)
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/logging.md` — Currency dimension (an unreferenced sibling in its own domain)
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/module_organisation.md` — Currency dimension (an unreferenced sibling in its own domain)
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/code_complexity.md` — Currency dimension (an unreferenced sibling in its own domain)
- `src/claude/_rules/05_lazy_load/style_guide_standards/python/python_standards.md` — Currency dimension (an unreferenced sibling in its own domain)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Broken link syntax:** "Related" uses `[[python_environment]]` — the memory system's wiki-link format, not a resolvable reference in a `_rules/` file, and it doesn't even carry the real relative path (`python/python_environment.md`).
- 🐛 **Domain disconnect:** unlike `airflow.md`/`dbt.md`, this parent has no "Child pages" table at all — 5 of its own domain's 6 detail files (`testing.md`, `logging.md`, `module_organisation.md`, `code_complexity.md`, `python_standards.md`) are never mentioned.
- 🐛 **Orphaned duplicate:** `python/python.md` is a near-identical copy of this parent file, unreferenced anywhere in the repo (confirmed via grep).
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
