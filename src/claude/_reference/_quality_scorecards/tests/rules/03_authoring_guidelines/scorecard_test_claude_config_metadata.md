# Quality Scorecard — test_claude_config_metadata.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-11

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | 2026-10-11 | • 🧮 **Raw complexity 1:** Concepts 0 (every rule's header, after any `paths:` frontmatter) + Scope 1 (`rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 1 test function and 3 assertions<br>• 🔀 **Split:** every rule is scanned here, while the format cases moved to `_core/test_metadata_header_format.py` on 2026-10-11 |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 3.0.0 updated 2026-10-11 |
| **Regression Value** | 8/10 | 2026-10-11 | • 🛡️ **Failure cases:** fails on any bad rule header, with the bad-input proofs in the shared format test |
| **Overall** | **9.0/10** | 2026-10-11 | • 💪 **Strongest:** Currency (10/10)<br>• ⚠️ **Weakest:** Regression Value (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/03_authoring_guidelines/test_claude_config_metadata.py` — the test being scored
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — what the test guards
