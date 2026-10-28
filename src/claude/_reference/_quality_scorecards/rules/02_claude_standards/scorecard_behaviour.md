# Quality Scorecard — behaviour.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.4/10

**Recommended improvements:**
- Move the "Other safety patterns" block (lines 47–59) under its own `##` heading with a Contents entry, so it no longer sits under "Before claiming completion".
- Make "Ask first", "Investigate" and "Read before claiming" (lines 49–51) live in one file only, either here or in `claude_response_standards.md` "Default Behaviour", and point to it from the other.
- Add at least one dated incident, issue number or usage record that shows these gates were needed.
- Cut line 11, which repeats the Purpose line, and rewrite line 63 as single-sentence, positively framed guidance.
- Move the `**Related:**` child bullet (line 58) out of the rule, and remove the blank line that splits the "Before proposing" list (line 66).
- Add a cross-reference test for each `**Loads on its own from:**` child pointer, not only `_artefact_proposal_gates.md`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear gates:** the complexity tiers, the risky-action list and the "take stated direction literally" example (lines 52–57) are concrete and easy to act on.<br>• ⚠️ **Misplaced block:** "Other safety patterns" (line 47) sits under "✅ Before claiming completion", but ask-first, investigate and plan approval have nothing to do with completion, and the Contents list doesn't show the block.<br>• ⚠️ **Two sources:** lines 49–51 repeat `claude_response_standards.md` "Default Behaviour" (ask before acting, investigate unfamiliar state, read before claiming), so the two files could drift and contradict each other.<br>• ⚠️ **Mixed list:** line 63 says "Flag any of the following", but the first item (line 65, Engineer test) is a question to ask, not a thing to flag, and a blank line separates it from the rest of the list. |
| **Complexity** | 6/10 | 2026-10-27 | • 🧮 **Raw complexity 4:** Concepts 3 (10 sections, 6 or more distinct behaviours) + Scope 1 (the parent plus its own `behaviour/` folder) + Dependencies 0 + Prerequisites 0.<br>• 🧮 **Anchor:** between the ~5 (raw 5) and ~7 (raw 3) rows, because it is an index of many concepts, even though each child holds one job. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ⚠️ **No recorded incident:** the file names no dated incident, issue or usage record.<br>• 🔗 **Partial support:** the `miss_cost: high` header (line 5) gives the cost of missing these gates, but no file shows the gates were ever missed.<br>• 🔗 **Plausible need:** safety defaults for irreversible actions are a reasonable precaution, but the anchor counts only what a file shows, so the score sits between ~5 (speculative) and ~7 (one dated incident). |
| **Token Cost Justification** | 9/10 | 2026-10-27 | • 🎯 **Justified always-on:** `applies_to: *` and `loading: always-on` (lines 4 and 6) are set, and safety gates apply to every session.<br>• 🎯 **Lean parent:** 8 of the 10 sections are one-line pointers to children.<br>• ⚠️ **Duplicate tokens:** lines 49–51 load twice per session, because `claude_response_standards.md` is also always-on. |
| **Structural Compliance** | 7/10 | 2026-10-27 | • ✅ **Within limits:** 98 counted lines after the 6 header lines, with a metadata header, an emoji H1 and H2s, a Purpose line and a Contents list justified by 10 headings.<br>• ⚠️ **Redundant line:** line 11 ("Rules governing how Claude acts safely…") repeats the Purpose line.<br>• ⚠️ **Style slips:** line 63 is a two-sentence paragraph ending in the negative "Do not proceed without explicit confirmation", and line 58 puts a `**Related:**` pointer inside the rule body.<br>• ⚠️ **Inconsistent Contents:** only some entries add a "(see `_x.md`)" note (lines 19, 21–24), so the index reads unevenly. |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **Paths exist:** every named file exists at commit 1705887: all 8 `behaviour/_*.md` children, `claude_plans.md`, `_rules_lazy_load/claude_config/hooks_decision_framework.md`, and `_decision_making.md`'s "User explicitly directs" bullet.<br>• 🔍 **Path prefix:** `~/.claude/` (line 69) follows the repo source convention (the other 13 "Read on demand" pointers under `02_claude_standards/` use it), and the install rewrites it.<br>• 🚩 **Pre-existing, outside the artefact:** `src/claude/_tests/README.md` line 54 credits `behaviour.md` with the "enforcement hooks need a test" rule, but that rule lives in `behaviour/_how_to_approach.md`. |
| **Test Coverage** | 8/10 | 2026-10-27 | • 🧪 **Structural:** `test_rules_structure.py` covers line limit, newline, H1/H2 emoji, Contents and Related-section checks.<br>• 🧪 **Content pointer:** `test_rule_cross_references.py` (lines 127–155) asserts that the parent still points to `_artefact_proposal_gates.md`.<br>• ⚠️ **Partial pointers:** the other 7 `Loads on its own from:` child pointers have no cross-reference assertion.<br>• ⚠️ **Not run here:** no test run is recorded for this review, and the reviewer is read-only, so the pass state was not checked. |
| **Overall** | **7.4/10** | 2026-10-27 | • 💪 **Strength:** a lean, current, always-on index whose risky-action and stated-direction guidance is concrete.<br>• ⚠️ **Gap:** it records no evidence of need, a misplaced "Other safety patterns" block mixes several jobs under one heading, and lines 49–51 duplicate `claude_response_standards.md`. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/behaviour.md` — the rule being scored
- `src/claude/rules/01_essentials/claude_response_standards.md` — Clarity and Token Cost (duplicated "Default Behaviour" bullets)
- `src/claude/rules/02_claude_standards/behaviour/_artefact_proposal_gates.md` — Currency and Test Coverage
- `src/claude/rules/02_claude_standards/behaviour/_before_acting.md` — Currency
- `src/claude/rules/02_claude_standards/behaviour/_decision_making.md` — Currency
- `src/claude/rules/02_claude_standards/behaviour/_how_to_approach.md` — Currency (the pre-existing `_tests/README.md` mis-credit)
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans.md` — Currency
- `src/claude/rules/_rules_lazy_load/claude_config/hooks_decision_framework.md` — Currency
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage
- `src/claude/_tests/README.md` — Currency (pre-existing mis-credit)
