# Quality Scorecard — claude_rule_loading_strategy.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Re-run `make audit_rule_usage` so `docs/audits/audit_rule_usage.md` uses the current folder names and has data from after the move, since the rule says to decide placement from that report.
- Say what "small" means in the Low / half-or-more cell (for example, a token threshold), so two readers place the same rule the same way.
- Split the "Folder sets the mode" bullet into two, and give each "When adding a rule" step a bold keyword.
- Add a test that checks the cut-offs (10 sessions, half, 90 days) against `MIN_SAMPLE_SESSIONS`, `DEMOTE_APPLIED_BELOW` and `STALE_AFTER_DAYS` in `audit_rule_usage.py`.
- Lower complexity by moving "Audit flags" into a lazy child, or into the audit report's own "How to read this" section.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 💪 **Decision matrix:** the miss-cost by applied-% table makes most placements mechanical<br>• ⚠️ **Undefined "small":** the "Always-on only if small" cell and step 4's "judging on criticality and size" give no threshold<br>• ⚠️ **Nesting:** the `02_claude_standards/` row says "Always-on" while `path_scoped_rules/` sits inside it, and only line 34's "unless a rule there has `paths:`" resolves this |
| **Complexity** | 4/10 | 2026-10-27 | • 🧮 **Raw complexity 6:** Concepts 2 (tier table, decision matrix, `paths:` fit, audit flags, adding steps) + Scope 2 (`rules/`, `_rules_lazy_load/`, `_reference/_style_guide_standards/`, `docs/audits/`) + Dependencies 1 (`make audit_rule_usage`) + Prerequisites 1 (a current audit report)<br>• ⚠️ **Five jobs:** "Audit flags" and "When adding a rule" are separate tasks from "which folder does a rule belong in" |
| **Evidence of Need** | 8/10 | 2026-10-27 | • 📈 **Recorded use:** `docs/audits/rule_usage_sessions.csv` records 35 applied sessions between 2026-08-31 and 2026-10-01<br>• 🔗 **Own placement:** `docs/audits/rule_usage_history.md` shows it missed in 35 of 35 sessions when it was purely lazy, which supports the `paths:` trigger it has now<br>• ⚠️ **No data since the move:** every row is from before the 2026-10-11 move to `path_scoped_rules/`, so whether it loads in its new place hasn't been measured |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** loads only with `**/rules/**`, `**/_rules_lazy_load/**`, `**/_style_guide_standards/**` or `**/CLAUDE.md`, so it's left out of the average |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Clean basics:** emoji headings, a Purpose line, the header in the right place, about 81 body lines, and `test_line_limit` / `test_ends_with_single_newline` cover the length and newline<br>• ⚠️ **Joined bullet:** line 34 puts two points in one bullet ("…unless a rule there has `paths:`…, and nothing under `rules/` is `@import`ed")<br>• ⚠️ **Steps with no keyword:** the numbered steps on lines 87–90 have no bold keyword |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Paths exist:** `make audit_rule_usage`, `test_rule_headers.py`, `test_path_scoped_rules_live.py`, `rule_usage_history.csv`, `_claude_config_metadata.md`, `authoring_agents.md` (has `paths:`) and every table example all resolve<br>• ⚠️ **Stale source:** line 42 says both deciding numbers are in `docs/audits/audit_rule_usage.md`, but that report was generated on 2026-10-01, still lists this rule as `05_lazy_load/`, and its miss-cost note says "— until Phase 5 adds them" |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Drift tests:** `test_claude_rule_loading_strategy.py` checks the five rows against the folders on disk, the order of the rows, that each example file exists, that each Loading cell matches its folder, the on-demand pointer, the length limit and the trailing newline<br>• ✅ **Enforced claims:** `test_high_cost_lazy_rules_load_mechanically` and the live `test_path_scoped_rules_live.py` back the "Pointers aren't triggers" and "Proven" bullets<br>• ⚠️ **Untested numbers:** nothing ties the decision matrix or the cut-offs (10, half, 90 days) to `audit_rule_usage.py`, so they match the script today only by luck |
| **Overall** | **7.2/10** | 2026-10-27 | • 💪 **Grounded:** a placement method backed by measured usage, with drift tests on its table<br>• ⚠️ **Gaps:** it relies on an audit report that's out of date, it does several jobs, and "small" is undefined |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_claude_rule_loading_strategy.py` — Test Coverage, Structural Compliance
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — Test Coverage
- `src/claude/_tests/rules/02_claude_standards/test_path_scoped_rules_live.py` — Test Coverage, Currency
- `src/claude/scripts/_audit_scripts/audit_rule_usage.py` — Test Coverage, Currency
- `docs/audits/audit_rule_usage.md` — Currency
- `docs/audits/rule_usage_sessions.csv` — Evidence of Need
- `docs/audits/rule_usage_history.md` — Evidence of Need
- `docs/audits/rule_usage_history.csv` — Currency
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — Currency
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/rules/03_authoring_guidelines/authoring_agents.md` — Currency
