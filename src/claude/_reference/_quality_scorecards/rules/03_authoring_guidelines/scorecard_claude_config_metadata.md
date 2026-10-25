# Quality Scorecard — _claude_config_metadata.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.7/10

**Recommended improvements:**
- Change line 60's "up to three more lines" to say which usage fields are required
- Update line 72's `path-scoped` definition to match `test_rule_headers.py` lines 345–346
- Add a test for line 24's bump-on-edit rule

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🎯 **Unambiguous core:** the three fields, the bump rules (lines 23–27) and the per-artefact placement table (lines 36–41) leave little room for different readings<br>• ⚠️ **Understated requirement:** `_claude_config_metadata.md` line 60 says entry-point rules "add up to three more lines", but line 69 makes `applies_to` required on always-on entry points and line 74 makes `loading` required on every entry point, so "up to" makes them sound optional |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (three fields, bump semantics, per-artefact placement, rule-only usage fields) + Scope 2 (rules, skills, agents and hooks across several folders) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`<br>• ⚠️ **Two jobs in one file:** lines 58–77 add a rule-only usage-field standard (`applies_to`, `miss_cost`, `loading`) on top of the shared header standard set out in line 11's Purpose |
| **Evidence of Need** | 7/10 | 2026-10-25 | • ✅ **Real consumers:** four header tests and `make audit_rule_usage` (line 75) depend on the format, so it is in active use<br>• ⚠️ **No dated problem:** line 20 ("git history doesn't travel with the live `~/.claude/` copy") gives a reason, but no incident or recorded failure is cited, and the 2026-09-28 note on line 53 is a design check, not a need |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • ✅ **Path-scoped, cost near zero:** `paths:` frontmatter (lines 1–5) keeps it out of non-config sessions, and line 53 records that HTML-comment headers cost no tokens<br>• ⚠️ **Broad trigger:** lines 3–4 (`**/.claude/**`, `**/claude/**`) match every file under the config, including reads unrelated to authoring, so in this repo it loads on almost any read |
| **Structural Compliance** | 9/10 | 2026-10-25 | • ✅ **Clean:** 78 lines, emoji H1, one-line Purpose, metadata header straight after `paths:`, bold-keyword one-sentence bullets, no Related section<br>• 🔍 **Not run:** compliance is judged from the file against `_hard_gates_checklist.md`, and `test_claude_config_metadata.py` covers it, but I didn't run that test this pass |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **References exist:** `testing_lazy_load/_test_metadata.md` (line 54) and `test_rule_headers.py` (line 73) both exist, and line 73's folder-match claim matches `expected_loading()` in that test<br>• ⚠️ **Drifted definition:** line 72 defines `path-scoped` as "lazy with `paths:` frontmatter", but this rule sits in tier 03 with `paths:`, and `test_rule_headers.py` lines 345–346 treat any rule with `paths:` as path-scoped wherever it lives<br>• 🔍 **Unverified:** `make audit_rule_usage` (line 75) falls outside the allowed inputs and was only seen named in `test_rule_headers.py` line 17 |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Mechanically enforced:** `test_claude_config_metadata.py` scans every rule header, `test_rule_headers.py` checks `applies_to`, `miss_cost` and `loading` against the folder, and the skill, agent, hook and shared-format header tests cover the other artefacts<br>• ⚠️ **Untested behaviour:** no test found checks line 24's "bump `version` on every edit, never change `created`" or line 23's new-artefact defaults, and I only grepped the skill, agent and hook test files, so line 51's contract-version match wasn't confirmed |
| **Overall** | **7.7/10** | 2026-10-25 | • 💪 **Strength:** one shared standard enforced by tests across all four artefact types<br>• ⚠️ **Gaps:** the rule-only usage fields widen the scope, line 72's path-scoped definition has drifted, and the bump-on-edit rule has no test |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — the rule being scored
- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — imports this file (Token Cost Justification)
- `src/claude/_tests/rules/03_authoring_guidelines/test_claude_config_metadata.py` — Test Coverage dimension
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — why the always-on import is required
