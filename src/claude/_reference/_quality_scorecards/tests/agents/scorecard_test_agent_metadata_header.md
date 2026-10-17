# Quality Scorecard — test_agent_metadata_header.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-17

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 8/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 7 test functions and 14 assertions<br>• 🧩 **Checks:** every AGENT.md header, version against maturity, and the template<br>• 🔀 **Split:** format cases moved to `_whole_config/test_metadata_header_format.py` on 2026-10-11 |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 2.0.0 updated 2026-10-11 |
| **Regression Value** | 9/10 | 2026-09-30 | • 🛡️ **Failure cases:** the maturity check proves a mismatched version is caught |
| **Overall** | **9.0/10** | 2026-09-30 | • 💪 **Strongest:** Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/agents/test_agent_metadata_header.py` — the test being scored
- `src/claude/agents/` — what the test guards
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — what the test guards
