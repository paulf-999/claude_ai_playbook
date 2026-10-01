# Quality Scorecard — testing.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.6/10

**Recommended improvements:**
- Add a check to `test_testing.py` that verifies the content-regression-test recommendation this file makes is itself followed somewhere in the test suite.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-28 | • 📋 **Clear exception logic:** instructional-content exception and content-regression-test recommendation are both well-explained<br>• 🔍 **Navigational defect:** Contents links to `#-child-files-load-as-needed`, but no heading with that text exists anywhere in the file |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** parent's own inline content covers 2 concepts (when tests are required, test goals), plus 5 imported children |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Load-bearing:** every other scorecard in this survey scores its own Test Coverage dimension using the exact exception clause this rule defines |
| **Token Cost Justification** | 10/10 | 2026-09-28 | • 🎯 **Scope:** Tier 2, always-on, blocking standard — unambiguously justified |
| **Structural Compliance** | 6/10 | 2026-09-28 | • ✅ **Compliant:** emoji headers, Purpose statement, trailing newline<br>• ❌ **Broken anchor:** confirmed via `grep "^## "` — no heading matches "Child Files (Load As Needed)"; the Contents entry doesn't correspond to any real section |
| **Currency** | 6/10 | 2026-09-28 | • 🔍 **Same root cause as above:** the Contents section wasn't updated when the file was restructured into its current 5 headings, leaving a dead link |
| **Test Coverage** | 7/10 | 2026-09-28 | • 🧪 **Direct test exists:** `test_testing.py`, 4 functions, validates that enforcement hooks have tests<br>• ⚠️ **Not exhaustive:** doesn't cover every rule this file states (e.g. the content-regression-test recommendation isn't itself checked) |
| **Overall** | **7.6/10** | 2026-09-28 | • 💪 **Strength:** foundational, load-bearing, clearly justified<br>• ⚠️ **Gap:** a broken internal anchor link in its own Contents section |

## 🔗 Related files

- `src/claude/_rules/02_claude_standards/testing.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_testing.py` — Test Coverage dimension

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Broken anchor:** the Contents section (line 9) links to `#-child-files-load-as-needed`, but no `##` heading in the file reads "Child Files (Load As Needed)" — confirmed via `grep "^## " testing.md`, which lists no such heading.
- 🚫 **Effect:** the link 404s within the rendered doc; a reader following Contents to find "child files" lands nowhere.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
