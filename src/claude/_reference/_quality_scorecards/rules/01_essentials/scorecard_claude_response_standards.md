# Quality Scorecard — claude_response_standards.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.1/10

**Recommended improvements:**
- Fix the contradiction between "Only Next steps" (line 61) and "Sources" (line 62): either allow sources in the "nothing between" rule or move them below the offer line.
- Define "short answers or casual exchanges" (lines 43 and 100) in the rule itself, for example the <50-word threshold already in the enforcement file.
- Say when "Speed prioritised" applies (line 67), so the Y/N/V offer line has a clear trigger.
- Move or point to the "Default Behaviour" section (lines 23–30) instead of repeating `behaviour.md` and `_how_to_approach.md` inline.
- Add a dated incident or usage record that shows the format problem recurs, beyond the undated "diluted to low-salience" claim.
- Add a test that keeps the hook's injected directive in step with this rule's Summary, offer-line and footer wording.
- Make bullet casing consistent after bold keywords, and use real `###` sub-headings in place of the bold pseudo-headings such as `**Summary structure (for substantive responses):**`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear format spec:** the Summary, Next steps, offer-line and footer rules are concrete and each has an example<br>• ⚠️ **Self-contradiction:** line 61 says only the Next steps block goes "between the Summary and the offer line", but line 62 puts sources "immediately before the offer line"<br>• ⚠️ **Undefined triggers:** "short answers or casual exchanges" (lines 43, 100) and "Speed prioritised" (line 67) have no test a reader can apply |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (6+ topics: default behaviour, Summary format, Next steps, narration, offer line, delivery cadence, timing) + Scope 0 (one file) + Dependencies 1 (the `UserPromptSubmit` hook) + Prerequisites 1 (the injected `PROMPT_SUBMITTED_AT` epoch)<br>• ⚠️ **Bundled concepts:** "Default Behaviour" and "Delivery Cadence" are conduct rules, not response format |
| **Evidence of Need** | 6/10 | 2026-10-25 | • 🔗 **Stated, not dated:** `miss_cost: medium — replies in the wrong shape, which the user asks to redo` (line 5) gives the cost but cites no incident<br>• ⚠️ **No usage record:** the enforcement file's "diluted to low-salience background" root cause has no date or example, which is short of the ~7 anchor's one dated incident |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • 🎯 **Earns always-on:** `applies_to: *` is set, and the rule shapes every substantive reply<br>• ⚠️ **Paid twice:** lines 25–29 (plan mode, ask before acting, investigate, read before claiming, respect scope) repeat always-on `behaviour.md` and `_how_to_approach.md`, and line 84 repeats `claude_operational_efficiency.md`'s "Parallel tool calls" |
| **Structural Compliance** | 7/10 | 2026-10-27 | • ✅ **Header and layout:** metadata lines 1–6, emoji H1, Purpose line, a Contents section that earns its place (5 `##` headings), and enforcement detail split into a lazy child<br>• ⚠️ **Near the limit:** 107 lines, inside the 110 tolerance but over the ~100 target<br>• ⚠️ **Style slips:** casing after bold keywords is mixed (capitalised in lines 25–30 and 79–84, lowercase in lines 37–49), and the bold pseudo-headings stand in for `###`<br>• ⚠️ **Inline duplication:** the "Default Behaviour" bullets copy other rules instead of pointing to them, which goes against `writing_style.md`'s "never duplicate inline" |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **References resolve:** `_before_acting.md`, `writing_style.md`, the `UserPromptSubmit` reminder hook and `response_standards_enforcement.md` all exist<br>• ✅ **Mechanism matches:** `PROMPT_SUBMITTED_AT` appears in the hook and its test, as the "Start is injected" bullet says |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Indirect coverage:** `test_style_guide_response_standards_reminder.py` checks that the injected directive carries `**Summary**`, `More detail? (Y/N)` and `Response time:`<br>• 🧪 **Placement test:** `test_rule_directory_organisation.py` pins the file as a top-level `01_essentials` rule<br>• ⚠️ **No sync check:** no test ties the hook's directive text to this rule's content, so the two can drift apart<br>• ⚠️ **Not run here:** the reviewer had no shell, so it couldn't confirm the `test_rules_structure.py` pass |
| **Overall** | **7.1/10** | 2026-10-27 | • 💪 **Concrete and enforced:** a precise output spec with examples, backed by a zero-cost per-turn injection hook<br>• ⚠️ **Scope creep and gaps:** the bundled conduct rules, one internal contradiction and undated evidence hold it back |

## 🔗 Related files

- `src/claude/rules/01_essentials/claude_response_standards.md` — the rule being scored
- `src/claude/rules/_rules_lazy_load/claude_config/response_standards_enforcement.md` — Evidence of Need, Clarity (the <50-word waiver), Test Coverage
- `src/claude/hooks/hook_style_guide_response_standards_reminder.sh` — Currency, Complexity (dependency)
- `src/claude/_tests/hooks/response_standards/test_style_guide_response_standards_reminder.py` — Test Coverage
- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — Test Coverage
- `src/claude/rules/02_claude_standards/behaviour.md` — Token Cost Justification, Structural Compliance (duplicated bullets)
- `src/claude/rules/02_claude_standards/behaviour/_how_to_approach.md` — Token Cost Justification (duplicated "respect scope")
- `src/claude/rules/02_claude_standards/behaviour/_before_acting.md` — Currency
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency.md` — Token Cost Justification (duplicated "Parallelise")
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
