# Quality Scorecard — test_confluence_create_page_timeout_options.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-06

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 8/10 | 2026-10-06 | • 🧮 **Raw complexity 2:** Concepts 1 (argument parsing, dialog wording, answers and the draft folder) + Scope 0 + Dependencies 0 + Prerequisites 1 (`tmp_path` and a patched config folder) |
| **Evidence of Need** | 7/10 | 2000-01-01 | • 🔗 **Target:** the confluence_create_page handler<br>• ⚠️ **Finding:** tests a Python handler kept beside the test, while the skill itself runs from its SKILL.md |
| **Coverage** | 10/10 | 2026-10-06 | • 📊 **Counts:** 17 test functions and 24 assertions<br>• 🧩 **Drafts:** they land in `~/claude/_drafts/confluence/` as `YYYY_MM_DD_<slug>.md`, a same-day redraft replaces the file, and the dialog names the folder |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-06 | • 🔍 **References:** matches the skill's `~/claude/_drafts/confluence/` folder as of 2026-10-06 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🐛 **Bug fixed:** drafts went to a hardcoded `~/.claude/_drafts/`, not the folder the skill and `writing_style.md` use |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Evidence of Need (7/10) |

## 🔗 Related files

- `src/claude/_tests/skills/confluence_create_page/test_confluence_create_page_timeout_options.py` — the test being scored
- `src/claude/_tests/skills/confluence_create_page/confluence_create_page_handler.py` — the handler under test
