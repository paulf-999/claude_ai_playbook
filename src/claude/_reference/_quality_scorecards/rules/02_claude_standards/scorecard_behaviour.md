# Quality Scorecard — behaviour.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.9/10

**Recommended improvements:**
- Make `_artefact_proposal_gates.md` line 12 and `_decision_making.md` line 23 give the same instruction on whether options follow passed gates
- Open the Risky actions section with the action to take, e.g. "Confirm before any of these, even on Trivial tasks"
- Add a dated incident to the parent or a child that shows each gate is needed
- Move the artefact proposal gates behind `paths:` or a read-on-demand pointer, since only authoring sessions need them
- Fix the style slips: the bold, emoji-less `Override signals` heading, bullets without a keyword in `_before_acting.md` and Gates 1 and 3, the semicolon-joined `**Why:**`, and "prioritizing"
- Correct the stale wording: the Gate 2 and Gate 3 Reference descriptions, and the "Processes" artefact type
- Extend `test_rule_cross_references.py` so it checks every `Loads on its own from:` pointer in `behaviour.md` resolves, as it already does for `git.md` and `claude_operational_efficiency.md`

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-28 | • ⚠️ **Contradiction:** `_artefact_proposal_gates.md` says "when every gate passes, the proposal proceeds without options", but `_decision_making.md` says "Options are presented *after* gates pass, not before"<br>• ⚠️ **No action in Risky actions:** the section lists Delete, Destructive git and the others, but never says what to do about them, so a reader has to connect it to the "Ask first" bullet higher up<br>• 🔍 **Clear tiers:** `_before_acting.md` names four tiers with examples and override signals, so two readers would pick the same tier |
| **Complexity** | 6/10 | 2026-10-28 | • 🧮 **Raw complexity 4:** Concepts 3 (six or more: tiers, verification, proposal flags, artefact gates, options, disclosure, model choice, conduct) + Scope 1 (the parent plus one children folder) + Dependencies 0 + Prerequisites 0<br>• ⚠️ **Wide family:** the parent and 7 children cover several separate jobs under one entry point |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ⚠️ **No dated incident:** none of the 8 files records an incident or usage, unlike `portable_paths.md` or `git/_concurrent_sessions.md`<br>• 🔗 **External sources only:** the support is the Karpathy principles cited in `_before_acting.md` and the Boris Cherny source comment in `_how_to_approach.md`, not problems this config observed |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • 🎯 **Headers set:** `applies_to: *`, `miss_cost: high` and a `loading:` reason are present, and confirmation gates apply to every session<br>• ⚠️ **Narrow child:** `_artefact_proposal_gates.md` (62 lines) is needed only when proposing a rule, skill, hook or agent, yet it loads every session |
| **Structural Compliance** | 7/10 | 2026-10-28 | • ✅ **Within length:** the parent is 96 lines excluding the 6 metadata lines, and each child is under 75 lines with a metadata header and Purpose line<br>• ⚠️ **Heading slip:** `_before_acting.md` line 28 `## **Override signals**` is bold and has no emoji<br>• ⚠️ **Bullet slips:** `_before_acting.md` "Example:" and "If YES → proceed" bullets, plus Gate 1 sub-bullets and Gate 3 bullets, have no bold keyword<br>• ⚠️ **Prose slips:** the parent's `**Why:**` joins two points with a semicolon, and `_session_conduct.md` uses "prioritizing" (American spelling) |
| **Currency** | 7/10 | 2026-10-28 | • ✅ **Paths exist:** `claude_plans.md`, `hooks_decision_framework.md`, `skill_domains.yaml`, the naming and directory-structure files and `technical_writer/AGENT.md` all exist<br>• ⚠️ **Stale description:** Gate 3 calls `claude_rule_loading_strategy.md` the "full rule index table", but that file now says each folder is the source of truth and holds no index<br>• ⚠️ **Stale description:** Gate 2 calls `_claude_directory_organisation.md` the "full tree", but that file says it is "not a comprehensive inventory"<br>• ⚠️ **Missing type:** Gate 1 names a "Processes" artefact with the example `session_kickoff.md`, and no such file or artefact type exists in `src/claude/` |
| **Test Coverage** | 8/10 | 2026-10-28 | • 🧪 **Gates covered:** `test_rule_cross_references.py` checks the gates' example skills, hook, agent, domains, tiers and reference files, plus synthetic bad cases<br>• 🧪 **Structure:** `test_rules_structure.py` and `test_rule_headers.py` cover file quality and headers, and with no incident recorded no content-regression test is required<br>• ⚠️ **Unchecked pointers:** only the gates pointer in `behaviour.md` is asserted, not its other six `Loads on its own from:` lines, whereas the `git.md` and efficiency children each have a resolve check |
| **Overall** | **6.9/10** | 2026-10-28 | • 💪 **Tiered gates:** proportional Trivial to Complex gates, with override signals and a confirmation floor for every tier<br>• ⚠️ **Conflict and evidence:** a direct contradiction between two children, and no recorded incident behind any gate |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/behaviour.md` — the rule being scored
- `src/claude/rules/02_claude_standards/behaviour/_before_acting.md` — Clarity, Structural Compliance
- `src/claude/rules/02_claude_standards/behaviour/_how_to_approach.md` — Evidence of Need
- `src/claude/rules/02_claude_standards/behaviour/_decision_making.md` — Clarity
- `src/claude/rules/02_claude_standards/behaviour/_artefact_proposal_gates.md` — Clarity, Token Cost Justification, Structural Compliance, Currency
- `src/claude/rules/02_claude_standards/behaviour/_pre_existing_issue_disclosure.md` — Complexity
- `src/claude/rules/02_claude_standards/behaviour/_session_conduct.md` — Structural Compliance
- `src/claude/rules/02_claude_standards/behaviour/_model_selection_strategy.md` — Complexity
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans.md` — Currency
- `src/claude/rules/_rules_lazy_load/claude_config/hooks_decision_framework.md` — Currency
- `src/claude/rules/03_authoring_guidelines/authoring_skills/skill_domains.yaml` — Currency, Test Coverage
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — Currency
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_directory_structure/_claude_directory_organisation.md` — Currency
- `src/claude/agents/core/technical_writer/AGENT.md` — Currency
- `src/claude/rules/02_claude_standards/claude_working_practices.md` — Evidence of Need (its children hold the dated-incident examples)
- `src/claude/rules/02_claude_standards/git/_concurrent_sessions.md` — Evidence of Need
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage
- `src/claude/_tests/rules/test_rule_headers.py` — Test Coverage
