# 📊 Scorecard Summary

**Purpose:** One-glance rollup of every rule scorecard's Overall score and whether it has Recommended improvements — see which rules need attention without opening each file individually.

---

## 📋 Current scores

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_portable_paths.md` | 9.4/10 | — (≥8.5) |
| `scorecard_claude_usage_standards.md` | 8.9/10 | — (≥8.5) |
| `scorecard_aliases.md` | 8.6/10 | — (≥8.5) |
| `scorecard_authoring_skills.md` | 8.6/10 | — (≥8.5) |
| `scorecard_guiding_principles.md` | 8.4/10 | • Raise `test_guiding_principles.py`'s assertion/function count |
| `scorecard_git.md` | 8.1/10 | • Fix the stale `_rules/claude_internal/git.md` reference in `test_git.py`'s docstring |
| `scorecard_claude_response_standards.md` | 7.9/10 | • Add a dedicated `test_claude_response_standards.py` structural test<br>• Cite a specific past incident that motivated this rule |
| `scorecard_behaviour.md` | 7.7/10 | • Add structural tests for the 5 untested children<br>• Document when a behavioral concept becomes its own child file vs. staying inline |
| `scorecard_security.md` | 7.6/10 | • Add a "Related rules" section cross-linking to `behaviour.md`<br>• Add dedicated tests for `_code_security.md` and the parent file |
| `scorecard_testing.md` | 7.6/10 | • Verify the content-regression-test recommendation this file makes is itself followed in the suite |
| `scorecard_claude_plans.md` | 7.6/10 | • Add a "Right" example alongside the existing "Wrong" example<br>• Add a Contents section, matching sibling tier files<br>• Add a dedicated test for `_plan_file_format.md` and the parent's own format |
| `scorecard_claude_operational_efficiency.md` | 7.1/10 | • Add structural tests for the parent and its 5 imported children<br>• Cite a specific incident that motivated this rule |
| `scorecard_authoring_rules.md` | 7.1/10 | • Extend `test_authoring_rules.py` to check tier names against the real directory structure |
| `scorecard_authoring_agents.md` | 6.9/10 | • Cite a specific incident or usage evidence for its always-on, Tier 3 placement |
| `scorecard_claude_rule_loading_strategy.md` | 6.4/10 | • Extend `test_rules_structure.py`'s emoji check to cover all `##` subheadings |

---

## 🔄 Keeping this current

- **Update on every scorecard change** — when a scorecard is created or re-scored (per `README.md`'s "When to score" cadence), update this file's row in the same commit. A summary that drifts from the underlying scorecards is worse than no summary — per `guiding_principles.md`'s own "False truth rots silently."
- **Sort order:** descending by Overall score — the rules needing the most attention are at the bottom.
- **Bullets are copied verbatim** from each file's own `**Recommended improvements:**` section (lightly trimmed for table width) — if you edit a bullet in one place, update the other.

---

## 🔗 Related

- `README.md` — the scorecard convention, template, and per-dimension criteria this file summarizes
- Individual `scorecard_*.md` files — full detail behind each row above
