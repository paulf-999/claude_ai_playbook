# Quality Scorecard — test_metadata_header_format.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-17

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-11 | • 🔍 **Messages:** every test function has a docstring, and every assertion says which case was wrongly accepted or rejected<br>• 🗂️ **Layout:** sections for the markdown header, the shell header and the header after frontmatter |
| **Complexity** | 8/10 | 2026-10-11 | • 🧮 **Raw complexity 2:** Concepts 2 (field format, placement, shell style, header after frontmatter) + Scope 0 (made-up inputs only) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-11 | • 🔗 **Target:** one standard for four artefact types, whose format cases were copied across four files until 2026-10-11 |
| **Coverage** | 10/10 | 2026-10-11 | • 📊 **Counts:** 23 test functions and 42 assertions<br>• 🧩 **Cases:** every field, order, semver and date rule, both comment styles, shebang placement, and frontmatter gaps |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff`<br>• 📁 **Location:** sits in `_tests/_whole_config/` with the other whole-config tests, importing the validator from `_tests/_helpers/` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current validator, header version 1.0.0 updated 2026-10-11 |
| **Regression Value** | 10/10 | 2026-10-11 | • 🛡️ **Failure cases:** 14 test functions prove a malformed or misplaced header is rejected |
| **Overall** | **9.4/10** | 2026-10-11 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/_whole_config/test_metadata_header_format.py` — the test being scored
- `src/claude/_tests/_helpers/_metadata_header.py` — the validator under test
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — the standard it checks
