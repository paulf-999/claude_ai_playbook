# Quality Scorecard — test_docs_local_links.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-11 | • 🔍 **Goal:** module docstring states what is skipped and cites issue #292<br>• ⚠️ **Messages:** only 2 of 14 assertions carry a failure message |
| **Complexity** | 8/10 | 2026-10-11 | • 🧮 **Raw complexity 2:** Concepts 1 (link extraction and resolution) + Scope 1 (`README.md` and `docs/` in the repo) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2026-10-11 | • 🔗 **Incident:** issue #292 found 52 links broken by folder moves, with nothing checking them |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 12 test functions and 14 assertions<br>• 🧩 **Cases:** web, mailto and anchor skips, fragments, folders, relative paths, titles, brackets and images |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 1.0.1 updated 2026-10-11 |
| **Regression Value** | 10/10 | 2026-10-11 | • 🛡️ **Failure cases:** a missing file is reported with its line, and every broken link on a line is listed |
| **Overall** | **9.0/10** | 2026-10-11 | • 💪 **Strongest:** Evidence of Need, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity (6/10) |

## 🔗 Related files

- `src/claude/_tests/_docs/test_docs_local_links.py` — the test being scored
- `README.md` — the repo README whose links it checks
- `docs/` — the docs folder whose links it checks
