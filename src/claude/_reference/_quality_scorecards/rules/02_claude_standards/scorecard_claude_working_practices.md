# Quality Scorecard — claude_working_practices.md

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 8.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-11 | • 📋 **Thin index:** names the three grouped rules and what each covers, with no rules of its own |
| **Complexity** | 8/10 | 2026-10-11 | • 🧮 **Raw complexity 2:** a pure 3-rule router with no inline guidance |
| **Evidence of Need** | 7/10 | 2026-10-11 | • 🗂️ **Housekeeping request:** groups three related rules so the tier root is easier to scan<br>• ⚠️ **No incident:** tidiness rather than a recorded failure |
| **Token Cost Justification** | 7/10 | 2026-10-11 | • 🪙 **One more startup file:** about 150 tokens every session, raising `MAX_STARTUP_FILES` from 42 to 43 for grouping alone |
| **Structural Compliance** | 9/10 | 2026-10-11 | • ✅ **Compliant:** metadata and usage headers, Contents matches headings, emoji headings, short (31 lines)<br>• 📁 **Grouping exemption:** listed in `GROUPING_DIRS` beside the `claude_usage_standards` precedent |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **New:** all three `Loads on its own from` paths resolve |
| **Test Coverage** | 8/10 | 2026-10-11 | • 🧪 **Indirect:** each grouped rule keeps its own tests (plans, operational efficiency, portable paths), and the folder is checked by `test_rule_directory_organisation.py`<br>• ⚠️ **Gap:** no test of the index's own content |
| **Overall** | **8.3/10** | 2026-10-11 | • 💪 **Strength:** follows an existing grouping precedent exactly<br>• ⚠️ **Gap:** costs a startup file for organisation only |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices.md` — the rule being scored
- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — Structural Compliance and Test Coverage dimensions
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Token Cost Justification dimension
