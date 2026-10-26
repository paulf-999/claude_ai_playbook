# Quality Scorecard — authoring_agents.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.7/10

**Recommended improvements:**
- Update `_core_standards.md` lines 30–32 to the `agents/<group>/<name>/AGENT.md` layout
- Make `_decision_tree_and_process.md` line 55 agree with the 5–8 draft eval count
- Fix the naming examples in `_core_standards.md` lines 22–25 and the "(below)" pointer on line 30
- Add an `applies_to` header so `make audit_rule_usage` can measure it

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-25 | • ⚠️ **Eval count contradicts itself:** `_decision_tree_and_process.md` line 55 says "8–12 test scenarios", but `_core_standards.md` lines 81 and 93 say Draft needs 5–8.<br>• ⚠️ **Naming examples break the pattern:** `_core_standards.md` lines 22–25 require `<domain>_<purpose>` but give `architect` as an example, and line 23 lists `technical_writer` as a "domain".<br>• ⚠️ **Wrong pointer:** `authoring_agents.md` line 30 says "Hard Gates Checklist (below)", but the checklist is a child file, not a section below. |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 (naming, frontmatter, structure, maturity, testing, decision tree, scope, mistakes), Scope 1 (governs `agents/`), Dependencies 0, Prerequisites 0.<br>• ⚠️ **Many concepts:** the parent plus 5 children in `_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/` cover 6 or more distinct concepts. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • 🔗 **Thin usage record:** the only evidence is in `test_authoring_agents.py` lines 14–20 ("used in 2 of 115 sessions", plus a 2026-09-28 audit gap).<br>• ⚠️ **No incident in the rule:** `authoring_agents.md` and its children record no dated problem that agents caused. |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • 🎯 **Path-scoped:** `paths: "**/agents/**"` (`authoring_agents.md` lines 2–3), and `test_parent_loads_with_agent_files` checks it isn't loaded at startup.<br>• ⚠️ **No applies_to:** the header (lines 5–9) has `miss_cost` and `loading` but no `applies_to`, so `make audit_rule_usage` can't measure it. |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Within limits:** the metadata header, emoji H1s, Purpose lines and one trailing newline are all present, and the longest child (`_core_standards.md`) is 101 lines.<br>• ⚠️ **Bullets without bold keywords:** `_core_standards.md` lines 22–26, and the Quick Navigation list in `authoring_agents.md` lines 19–31.<br>• ⚠️ **Two-sentence Purpose:** `authoring_agents.md` line 12. |
| **Currency** | 6/10 | 2026-10-25 | • 🍂 **Old agent layout:** `_core_standards.md` lines 30–32 give the filename as `<domain>_<purpose>.md` (e.g. `agents/core/technical_writer.md`) and say "flexible for now", but the current convention is `agents/<group>/<name>/AGENT.md`.<br>• ⚠️ **Unverified template:** `_core_standards.md` line 73 points to `AGENT.md.template`, which is outside the allowed inputs, so I couldn't confirm it exists.<br>• ⚠️ **Prefix mismatch:** `authoring_agents.md` lines 40–44 use `~/.claude/_rules_lazy_load/...`, while the live sibling rules use `~/claude/`. This is only a gap if the install doesn't rewrite the prefix. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Dedicated structural test:** `_tests/rules/03_authoring_guidelines/test_authoring_agents.py` checks the pointers, that each child exists and nothing extra is on disk, the H1s, Purpose lines, newlines, `paths:` and the pointer from `authoring_rules.md`.<br>• ⚠️ **Not run in this review:** I didn't confirm a pass, and `test_rules_structure.py` was outside the allowed inputs. |
| **Overall** | **6.7/10** | 2026-10-25 | • 💪 **Strength:** it is properly path-scoped, its children are read on demand, and a dedicated test guards how they are wired.<br>• ⚠️ **Gap:** the children contradict each other (eval counts, naming) and describe an old agent file layout. |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/authoring_agents.md` — the rule being scored
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_agents.py` — Test Coverage dimension
- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — sibling authoring guide, for comparison
- `src/claude/rules/03_authoring_guidelines/authoring_skills.md` — sibling authoring guide, for comparison
