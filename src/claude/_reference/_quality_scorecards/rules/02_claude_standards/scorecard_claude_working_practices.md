# Quality Scorecard — claude_working_practices.md

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-27

**Overall score:** 7.6/10

**Recommended improvements:**
- Add a test that checks each of this index's three `**Loads on its own from:**` pointers resolves, and that no sibling under `claude_working_practices/` is left unnamed, modelled on `test_efficiency_children_resolve_inside_their_folder` and `test_git_points_to_every_child`.
- Record why the group needs its own always-on index file, with a dated problem, an issue link or a usage note, given that each child already loads natively.
- Name the efficiency section to match its child's H1 ("Operational efficiency" here, "Claude Operational Discipline" in the child), or rename the child's H1.
- Put `---` dividers between all three sections, as already done after Purpose and Contents, or remove them everywhere.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear index:** the Purpose line and each Contents entry say what each child covers in one line.<br>• ⚠️ **Name drift:** the section `## 🔧 Operational efficiency` points to a child whose H1 is "🔧 Claude Operational Discipline", so a reader may not match them up. |
| **Complexity** | 8/10 | 2026-10-25 | • 🧮 **Raw complexity 2:** Concepts 1 (three pointers) + Scope 1 (one child directory) + Dependencies 0 + Prerequisites 0. |
| **Evidence of Need** | 6/10 | 2026-10-27 | • 🔗 **Borrowed evidence:** the `miss_cost` line ("uncapped automation and non-portable hooks fail before anyone notices") describes the children's need, not the need for this index.<br>• ⚠️ **No index-level record:** the only dated trace is the budget comment in `test_always_on_reachability.py` ("42 -> 43 on 2026-10-11: claude_working_practices.md indexes the plans, efficiency and portable-paths group"), which records that it was added, not a problem it solved. |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • 🎯 **Small and set:** about 25 content lines, with `applies_to: *` and a `loading:` reason recorded.<br>• ⚠️ **Navigation only:** each child already loads natively, so this file adds one startup file (it raised `MAX_STARTUP_FILES` from 42 to 43) and holds no guidance of its own. |
| **Structural Compliance** | 8/10 | 2026-10-25 | • ✅ **Conventions met:** it has the metadata header, emoji H1 and H2s, a one-line Purpose, Contents for exactly 3 real headings, and bold-keyword pointer bullets.<br>• ⚠️ **Divider slip:** `---` sits after Purpose and after Contents but not between the three sections.<br>• ⚠️ **Unverified run:** no file in this review records a `test_rules_structure.py` pass at commit 1705887. |
| **Currency** | 9/10 | 2026-10-25 | • ✅ **All paths exist:** `claude_plans.md`, `claude_operational_efficiency.md` and `portable_paths.md` are all in `rules/02_claude_standards/claude_working_practices/`.<br>• ✅ **Contents accurate:** the one-line summaries match the children's current sections (plan gates and file format; token awareness, delegation, turn budgets and automation controls; portable paths). |
| **Test Coverage** | 7/10 | 2026-10-27 | • 🧪 **Generic only:** it is covered by `test_rules_structure.py` and the startup budget in `test_always_on_reachability.py`.<br>• ⚠️ **Pointers untested:** no test checks this file's `Loads on its own from` lines, since the only regex for that form (`LOADS_ON_ITS_OWN` in `test_rule_cross_references.py`) runs against `claude_operational_efficiency.md` alone.<br>• 🧪 **No incident:** the file documents no incident, so it needs no content-regression test. |
| **Overall** | **7.6/10** | 2026-10-27 | • 💪 **Current and lean:** a short, accurate index whose every pointer resolves today.<br>• ⚠️ **Thin justification:** an always-on navigation file with no evidence of its own need and no test of its pointers. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans.md` — Currency
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency.md` — Clarity and Currency
- `src/claude/rules/02_claude_standards/claude_working_practices/portable_paths.md` — Currency
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Evidence of Need, Token Cost and Test Coverage
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance and Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
