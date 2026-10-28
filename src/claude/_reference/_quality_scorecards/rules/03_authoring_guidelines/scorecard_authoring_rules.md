# Quality Scorecard — authoring_rules.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.0/10

**Recommended improvements:**
- Replace the "~100–150 tokens/session cost" figure on line 22 with a measured one, or remove it.
- Correct the `02_claude_standards/` tier description so it no longer lists `testing`, which lives in `path_scoped_rules/`.
- Move the always-on rule to `paths:` loading that matches its `applies_to`, or write down why sessions that never touch a rule still need it.
- Put one dated incident or PR from `_common_mistakes.md` into the rule itself as its evidence.
- Split the semicolon-joined bullets on lines 63 and 66 into child bullets, and make the punctuation of the five creation steps match.
- Add cross-reference tests for the `claude_rule_loading_strategy.md`, `_claude_config_metadata.md` and `_complexity_scoring.md` pointers, and for the `quality_scorecard_reviewer` agent.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-27 | • 🔍 **Actionable flow:** the 5-question checklist, then 5 steps, then the gates, reads in order and can be followed as written<br>• ⚠️ **Loose pointers:** lines 69 and 71 sit apart from the gate list, and line 71 never says why the complexity formula matters when writing a rule |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (checklist, creation steps, quality gates, scorecard, on-demand children) + Scope 2 (rules tiers, `_tests/`, `_templates/`, `_reference/`) + Dependencies 0 + Prerequisites 0 — see `_complexity_scoring.md` |
| **Evidence of Need** | 7/10 | 2026-10-27 | • ✅ **Shipped mistakes:** `_common_mistakes.md` cites PR #94 (stale tier names) and PR #97 (missing metadata headers)<br>• ⚠️ **Not in the rule:** the parent names no incident, PR or usage record of its own, and the child's PRs have no dates |
| **Token Cost Justification** | 6/10 | 2026-10-25 | • ⚖️ **Justified in a comment:** the line 6 `loading:` comment says a new rule can start before any rule file is open<br>• ⚠️ **Wider than its scope:** `applies_to` (line 4) is `**/rules/**, **/_rules_lazy_load/**`, but the file loads every session<br>• ⚠️ **Cost figure looks wrong:** line 22 quotes "~100–150 tokens/session" for always-on rules, but this 78-line file alone is far larger |
| **Structural Compliance** | 7/10 | 2026-10-27 | • ✅ **Header and length:** metadata in lines 1–3, H1 with emoji, a one-line Purpose, and 78 lines, under the limit<br>• ⚠️ **Style slips:** lines 63 and 66 join two statements with a semicolon instead of using child bullets<br>• ⚠️ **Uneven steps:** only step 4 (line 51) ends with a full stop, and line 11 is two prose sentences outside the bullets<br>• ⚠️ **Not run:** the reviewer didn't run `test_rules_structure.py`, so a pass isn't confirmed |
| **Currency** | 7/10 | 2026-10-27 | • ✅ **Paths exist:** the template, `claude_rule_loading_strategy.md`, `authoring_agents.md`, both `shared_standards/` children, all three on-demand children, `test_always_on_reachability.py` and the `quality_scorecard_reviewer` agent are all there at commit 1705887<br>• ⚠️ **Tier drift:** line 39 lists `testing` under `02_claude_standards/`, but `testing.md` is at `02_claude_standards/path_scoped_rules/testing.md` |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Runnable tests:** `test_rule_cross_references.py` checks the template, tiers, scorecard README, three on-demand children and the structural test, and `test_authoring_agents.py` checks the agent-guide pointer<br>• ⚠️ **Unchecked pointers:** no test covers the loading-strategy, metadata or complexity-scoring pointers, or the reviewer agent name on line 52<br>• ⚠️ **Not run:** the reviewer didn't run these tests |
| **Overall** | **7.0/10** | 2026-10-25 | • 💪 **Well tested:** most of the references the rule names are checked by tests that actually run<br>• ⚠️ **Always-on cost:** the rule loads every session, but its own `applies_to` covers only rule-authoring files |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — the rule being scored
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity, Clarity
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — Test Coverage
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_rules/_common_mistakes.md` — Evidence of Need
- `src/claude/rules/02_claude_standards/path_scoped_rules/testing.md` — Currency
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — Currency, Test Coverage
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_agents.py` — Test Coverage
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance, Test Coverage
- `src/claude/agents/core/quality_scorecard_reviewer/AGENT.md` — Currency, Test Coverage
