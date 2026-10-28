# Quality Scorecard — git.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.9/10

**Recommended improvements:**
- Settle the `gh` CLI vs GitHub MCP bullet (line 66): say plainly whether MCP is allowed once access is confirmed, or never.
- Make "Simplest over proper" (line 44) testable by saying when a stash or reset is the right call.
- Rewrite the negative bullets (lines 45, 66, 74) as positive actions, and split the semicolon-joined Title format bullet (line 71) into child bullets.
- Add a dated incident or usage record for the parent's own sections (Complex Git Operations, Protected Branches, PR size limit) to the rule or a usage file.
- Narrow `applies_to: *` or record why the branch-naming and PR sections need to load in sessions that never touch git.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-27 | • 🔍 **Mostly actionable:** branch prefixes, the regex, the PR size limit and the title format are exact and can be checked.<br>• ⚠️ **Mixed signal:** line 66 says to use `gh` "for all GitHub PR operations" but then allows MCP "without first confirming access", so two readers could disagree on whether MCP is ever allowed.<br>• ⚠️ **Judgement call:** line 44's "simplest correct option over the most 'proper' one" gives one example but no test for when a stash is acceptable. |
| **Complexity** | 6/10 | 2026-10-27 | • 🧮 **Raw complexity 4:** Concepts 2 (four of its own sections: complex ops, protected branches, branch naming, PRs) + Scope 1 (the `git/` folder holds three children) + Dependencies 1 (`gh` CLI and the PR template) + Prerequisites 0.<br>• ⚠️ **Wide index:** counting the three children it points to, the topic covers 6+ concepts, which is close to raw 5. |
| **Evidence of Need** | 7/10 | 2026-10-25 | • ✅ **One dated incident:** the child `git/_concurrent_sessions.md` records the 2026-09-21 contaminated-commit incident.<br>• ✅ **Enforced in practice:** `.pre-commit-config.yaml` (`no-commit-to-branch`) and `src/sh/pre_commit_hooks/git_validate_branch_name.sh` show the branch rules are used.<br>• ⚠️ **No record for the parent's own sections:** no file records an incident or repeat use behind Complex Git Operations, the 20-file PR limit or the plain-language PR title rule. |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • 🎯 **Justified always-on:** the header sets `applies_to: *` and `miss_cost: high` and gives a reason ("commits can happen in any session").<br>• ⚠️ **Broad load:** the branch-naming and PR sections (lines 55–74) matter only in git or PR sessions, but they load everywhere. |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Clean shell:** has the metadata header, an H1 emoji, a Purpose line and emoji headings, runs 75 lines, and names each child in a `**Loads on its own from:**` line.<br>• ⚠️ **Style slips:** line 71 joins two points with a semicolon in one bullet.<br>• ⚠️ **Negative framing:** lines 45 ("do not drop or pop"), 66 ("do not attempt") and 74 ("must not contain") break the house style's positive-framing rule. |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **Every reference exists:** all three children (`_safe_patterns.md`, `_commits.md`, `_concurrent_sessions.md`) and `.github/pull_request_template.md` are on disk.<br>• ✅ **Pattern matches enforcement:** the regex on line 59 is the same one in `git_validate_branch_name.sh`. |
| **Test Coverage** | 9/10 | 2026-10-27 | • 🧪 **Content tests:** `test_rule_cross_references.py` checks that each child pointer is present, that each child exists, that the branch examples match the regex, and that bad names fail it.<br>• 🧪 **Mechanical enforcement:** the pre-commit hook and `no-commit-to-branch` enforce the branch rules.<br>• ⚠️ **Not run by the reviewer:** it had no shell, so this score relies on the tests and hooks on disk, not on an observed pass. |
| **Overall** | **7.9/10** | 2026-10-27 | • 💪 **Strength:** concrete, machine-checkable branch rules that tests and a pre-commit hook back up.<br>• ⚠️ **Gap:** the parent's own guidance has no recorded evidence, and there are a few clarity and style slips. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/git.md` — the rule being scored
- `src/claude/rules/02_claude_standards/git/_safe_patterns.md` — child it points to (Currency)
- `src/claude/rules/02_claude_standards/git/_commits.md` — child it points to (Currency)
- `src/claude/rules/02_claude_standards/git/_concurrent_sessions.md` — child with the 2026-09-21 incident (Evidence of Need)
- `src/claude/_tests/rules/test_rule_cross_references.py` — git.md child and branch-pattern tests (Test Coverage)
- `src/claude/_tests/rules/02_claude_standards/test_concurrent_sessions.py` — reachability and incident-record test (Test Coverage)
- `src/claude/_tests/rules/test_rules_structure.py` — structural test (Test Coverage)
- `src/sh/pre_commit_hooks/git_validate_branch_name.sh` — branch regex enforcement (Evidence of Need, Currency)
- `.pre-commit-config.yaml` — `no-commit-to-branch` hook (Evidence of Need)
- `.github/pull_request_template.md` — PR template the rule names (Currency)
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — complexity formula (Complexity)
