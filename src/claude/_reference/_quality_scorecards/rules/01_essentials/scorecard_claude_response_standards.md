# Quality Scorecard — claude_response_standards.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 7.6/10

**Recommended improvements:**
- Move the Delivery Cadence section to `behaviour.md` or `claude_operational_efficiency.md`, because it governs how Claude works and the rule's own Scope line limits it to how replies look.
- Define "substantive" inside the rule and make the skip criteria match `response_standards_enforcement.md`, including its under-50-words threshold and its skill-output waiver.
- Say whether "Wait: get an explicit reply" applies in non-interactive runs (subagents, `/goal`, `/loop`).
- Split the semicolon-joined Human-readable format bullet into two child bullets.
- Make capitalisation after the colon consistent in the Delivery Cadence and Response Timing bullets.
- Move the "Anti-pattern" bullet out of the Follow-up offer list.
- Record a passing run of `test_rules_structure.py` and `test_rule_headers.py` for this file.
- Add a dated incident (when Claude Code replies missed the format) to back up the evidence of need.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Concrete format:** the Summary, Next steps, offer-line and footer rules each have a worked example, so two readers would build the same reply<br>• ⚠️ **Undefined threshold:** "substantive responses" (line 27) and "Short, single-fact answers" (line 90) are not defined in the rule, while `response_standards_enforcement.md` uses "<50 words" and adds skill-output, code-output and error waivers that the rule doesn't mention<br>• ⚠️ **Scope contradiction:** line 24 says the rule "covers only how replies look", but Delivery Cadence (lines 70–74) governs how Claude works ("Minimise digging", "Fastest correct path")<br>• ⚠️ **Wait in non-interactive runs:** "Wait: get an explicit reply before proceeding" (line 61) doesn't say how it applies to subagents or `/goal` runs |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (Summary, Next steps, narration, research acknowledgement, offer line, cadence and timing, so 6+) + Scope 0 (one file) + Dependencies 1 (the `UserPromptSubmit` hook that injects `PROMPT_SUBMITTED_AT`) + Prerequisites 1 (hook registered in `settings.json`)<br>• ⚠️ **Extra concern:** Delivery Cadence is a separate job, and moving it out would reduce the concept count |
| **Evidence of Need** | 7/10 | 2026-10-28 | • 🔗 **Observed failure:** `response_standards_enforcement.md` records that the always-on rule is "diluted to low-salience background" in Claude Code but enforces reliably in Desktop, and the per-turn injection hook was built to fix this<br>• 📊 **Load data:** `docs/audits/audit_rule_usage.md` shows the rule applied in 115 of 115 sessions, with 11 misses<br>• ⚠️ **Undated:** no file gives a date or incident for replies that broke the format, so this sits at the one-real-problem anchor and not the recurring-incident anchor |
| **Token Cost Justification** | 9/10 | 2026-10-28 | • 🎯 **Justified:** `applies_to: *` and `miss_cost: medium`, and the audit shows 100% applied (115 sessions), which the loading-strategy table places in always-on<br>• 💸 **Size:** 1,562 tokens per session, with a compact copy also injected each turn by `hook_style_guide_response_standards_reminder.sh` on purpose |
| **Structural Compliance** | 8/10 | 2026-10-28 | • ✅ **Shape:** H1 emoji, Purpose line, metadata header including `applies_to`, `miss_cost` and `loading`, a Contents section earned by 4 `##` headings, and 97 lines in total<br>• ⚠️ **Joined bullet:** line 85 joins two clauses with a semicolon ("Under 60 seconds show `Ss` …; 60 seconds or more show …")<br>• ⚠️ **Style slips:** capitalisation after the colon is inconsistent ("Share", "On", "Avoid", "The" in lines 70–90 against lowercase elsewhere), and the "Anti-pattern" bullet (line 64) sits inside the Follow-up offer list |
| **Currency** | 9/10 | 2026-10-28 | • 🔍 **References exist:** `behaviour.md`, `writing_style.md` and `_rules_lazy_load/claude_config/response_standards_enforcement.md` all exist<br>• ✅ **Matches the hook:** `hook_style_guide_response_standards_reminder.sh` is registered under `UserPromptSubmit` in `settings.json` and injects `PROMPT_SUBMITTED_AT`, as the rule says |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural:** covered by `test_rules_structure.py` and `test_rule_headers.py`, and no content-regression test is needed because the rule records no incident<br>• 🧪 **Mechanism:** `test_style_guide_response_standards_reminder.py` checks the injected directive and the `PROMPT_SUBMITTED_AT` timestamp<br>• ⚠️ **Pass not shown:** this review found no record that these tests pass for this file at c638e09 |
| **Overall** | **7.6/10** | 2026-10-28 | • 💪 **Format and enforcement:** a precise reply format backed by a registered, tested per-turn injection hook<br>• ⚠️ **Scope and skip rules:** Delivery Cadence is outside the rule's stated scope, and the skip criteria don't match the enforcement file |

## 🔗 Related files

- `src/claude/rules/01_essentials/claude_response_standards.md` — the rule being scored
- `src/claude/rules/_rules_lazy_load/claude_config/response_standards_enforcement.md` — Clarity (different skip criteria), Evidence of Need (dilution finding), Currency
- `src/claude/hooks/hook_style_guide_response_standards_reminder.sh` — Complexity, Token Cost, Currency
- `src/claude/settings.json` — Complexity, Currency (hook registration)
- `src/claude/rules/02_claude_standards/behaviour.md` — Clarity (where Delivery Cadence belongs), Currency
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance, Currency
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — Token Cost Justification
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `docs/audits/audit_rule_usage.md` — Evidence of Need, Token Cost Justification
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — Test Coverage
- `src/claude/_tests/hooks/response_standards/test_style_guide_response_standards_reminder.py` — Test Coverage
