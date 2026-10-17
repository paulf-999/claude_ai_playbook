# Quality Scorecard — test_skill_metadata_header.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-17

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 8/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 4 test functions and 7 assertions<br>• 🧩 **Checks:** every SKILL.md header, its match with `skill.contract.yaml`, and the template<br>• 🔀 **Split:** format cases moved to `_whole_config/test_metadata_header_format.py` on 2026-10-11 |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 2.0.0 updated 2026-10-11 |
| **Regression Value** | 8/10 | 2026-10-11 | • 🛡️ **Failure cases:** fails on any bad skill header or contract mismatch, with the bad-input proofs in the shared format test |
| **Overall** | **8.9/10** | 2026-10-11 | • 💪 **Strongest:** Currency (10/10)<br>• ⚠️ **Weakest:** Complexity and Regression Value (8/10) |

## 🔗 Related files

- `src/claude/_tests/skills/_skill_standards/test_skill_metadata_header.py` — the test being scored
- `src/claude/skills/` — what the test guards
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — what the test guards
