# Quality Scorecard — claude_response_standards.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.9/10

**Recommended improvements:**
- Resolve the footer contradiction between line 93 ("never skip") and line 100 (skip for short answers)
- Define "substantive" in the always-on rule, not only in the lazy child
- Move Default Behaviour and Delivery Cadence out of a file about response format
- Give the Summary bullets bold keywords and split the two-sentence bullet on line 92

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Contradiction:** `claude_response_standards.md` line 93 says "never skip" the timing footer, but line 100 says to skip it for short answers.<br>• ⚠️ **Undefined trigger:** "substantive" (line 36) is defined only in the child `response_standards_enforcement.md` line 28, so a reader of the always-on rule alone can't tell when the Summary applies.<br>• 🌫️ **Fuzzy limit:** line 39's "≤~15 words (~100 chars)" gives a soft bound that two readers could apply differently. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (default behaviour, summary format, next steps, offer line, delivery cadence, timing) + Scope 1 (parent plus child in `_rules_lazy_load/claude_config/`) + Dependencies 1 (the `UserPromptSubmit` hook, line 91) + Prerequisites 0.<br>• ⚠️ **Several jobs:** lines 23–30 (Default Behaviour) and 78–85 (Delivery Cadence) are about conduct, not response shape, so the file does more than one job. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ❓ **No incident in rule:** the parent records no dated incident or usage evidence.<br>• 🔗 **Partial rationale:** the child's lines 17–19 explain the salience problem (Desktop vs CLI) but give no date, issue or count of times it happened. |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • ✅ **Justified placement:** line 4 `applies_to: *` matches a standard that shapes every reply.<br>• 💸 **Off-concept bulk:** lines 23–30 (Default Behaviour) add always-on cost for guidance that isn't response format. |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and length:** metadata lines 1–6, an emoji H1, a Purpose line and about 100 counted lines are all present.<br>• 📏 **Missing bold keywords:** lines 37–72 are bullets with no leading bold keyword.<br>• 📏 **Multi-sentence bullet:** line 92 holds two sentences, which breaks the "one sentence per bullet" gate.<br>• 📏 **Stray anti-pattern:** line 74's "Anti-pattern" line is a loose fragment rather than a bullet.<br>• ⚠️ **Hardcoded path:** line 106 uses a literal `~/.claude/` path, against the hard gate's "No hardcoded paths" item.<br>• ⚠️ **One concept:** the file covers four distinct concepts, which misses that hard gate. |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Paths exist:** `_before_acting.md`, `writing_style.md`, the child file and `hooks/hook_style_guide_response_standards_reminder.sh` all exist.<br>• 🍂 **Stale wording in child:** `response_standards_enforcement.md` line 17 says "always-on rule import", but rules now load natively and are not imported. |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Structural coverage exists:** `test_rules_structure.py` and `test_rule_headers.py` exist. `test_rule_directory_organisation.py` line 33 names the file. Not run in this review.<br>• 🧪 **Hook tested:** `test_style_guide_response_standards_reminder.py` lines 121 and 157 assert the injected `PROMPT_SUBMITTED_AT` start time.<br>• ⚠️ **No sync test:** no test ties the rule's own text (e.g. the `Mmin Ss` format at line 95) to the hook's directive, so the two can drift. |
| **Overall** | **6.9/10** | 2026-10-25 | • 💪 **Mechanised:** a per-turn injection hook backs the rule, and that hook has tests.<br>• ⚠️ **Bundled and slipping:** non-format conduct sections, style slips, the footer skip contradiction and no recorded evidence hold it back. |

## 🔗 Related files

- `src/claude/rules/01_essentials/claude_response_standards.md` — the rule being scored
- `src/claude/_tests/hooks/response_standards/test_style_guide_response_standards_reminder.py` — Test Coverage dimension
- `src/claude/_tests/hooks/response_standards/test_style_guide_response_standards_checker_flags.py` — Test Coverage dimension
- `src/claude/_tests/hooks/response_standards/test_style_guide_response_standards_checker_waivers.py` — Test Coverage dimension
