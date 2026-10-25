# Quality Scorecard — git.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.6/10

**Recommended improvements:**
- Correct `git/_safe_patterns.md` line 18, since `git -C <repo>` still runs that repo's hooks
- Make `_commits.md` line 25 and `_concurrent_sessions.md` line 24 agree on `git add -A`
- Convert the prose in `_safe_patterns.md` and `_concurrent_sessions.md` line 12 to one-sentence bullets
- Update `test_concurrent_sessions.py` line 27's stale `@import` message

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Actionable:** most bullets give a concrete command or regex, such as the branch pattern at `git.md` line 59.<br>• ⚠️ **Staging conflict:** `git/_commits.md` line 25 says never `git add -A` "without review", but `git/_concurrent_sessions.md` line 24 says never `git add -A`, with no exception, and claims the two say the same thing.<br>• ⚠️ **No fallback:** `git.md` line 67 says always use `.github/pull_request_template.md`, but doesn't say what to do in a repo that has none. |
| **Complexity** | 4/10 | 2026-10-25 | • 🧮 **Raw complexity 6:** Concepts 3 (seven topics in `git.md` lines 13–19), Scope 1 (a parent plus one child folder), Dependencies 2 (git, `gh` at line 66, `pre-commit` at `git/_commits.md` line 15), Prerequisites 0.<br>• ⚠️ **Bundled:** branch naming, PR rules and the concurrent-session incident sit together in one always-on rule tree. |
| **Evidence of Need** | 7/10 | 2026-10-25 | • ✅ **One dated incident:** `git/_concurrent_sessions.md` line 12 records the 2026-09-21 contaminated-index incident.<br>• ⚠️ **Unbacked children:** `git/_safe_patterns.md`, `git/_commits.md` and `git.md` lines 41–74 cite no incident, PR or repeated failure. |
| **Token Cost Justification** | 8/10 | 2026-10-25 | • 🎯 **Headers set:** `git.md` lines 4–6 give `applies_to: *`, a high `miss_cost` and a loading reason.<br>• ⚠️ **Every session pays:** with `applies_to: *` at line 4, about 170 lines across the four files load even in sessions that never commit, including the PR rules at lines 64–74 and the incident story at `git/_concurrent_sessions.md` line 12. |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Basics met:** every file has the metadata header, an emoji H1 and a Purpose line, and stays under 110 lines.<br>• ❌ **Prose, not bullets:** `git/_safe_patterns.md` lines 12–24 are paragraphs, and lines 16 and 18 each hold two sentences.<br>• ❌ **Multi-sentence prose:** `git/_concurrent_sessions.md` line 12 is a four-sentence paragraph, and line 25 joins two clauses with a semicolon.<br>• ⚠️ **No bold keyword:** the sub-bullets at `git/_commits.md` lines 20–23 open without one.<br>• ⚠️ **Repeated heading:** the H2 at `git/_commits.md` line 10 just repeats the H1. |
| **Currency** | 6/10 | 2026-10-25 | • ✅ **Children exist:** the three child pointers at `git.md` lines 25, 31 and 37 are checked by `test_git_children_exist`.<br>• ❌ **Wrong claim:** `git/_safe_patterns.md` line 18 says `git -C` removes the hook risk, but `git -C <repo>` still runs that repo's `.git/hooks/`.<br>• ⚠️ **Drifted cross-reference:** `git/_concurrent_sessions.md` line 24 says `_commits.md` already requires the same thing, but `_commits.md` line 25 allows `git add -A` after review. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Incident test:** `_tests/rules/02_claude_standards/test_concurrent_sessions.py` lines 37–43 keep the incident's key phrases, tagged `# wording-check:`.<br>• 🧪 **Cross-references:** `_tests/rules/test_rule_cross_references.py` lines 263–290 check the child pointers, that the children exist, and that the branch regex accepts its examples and rejects bad names.<br>• ⚠️ **Stale message:** `test_concurrent_sessions.py` line 27 still mentions `@import`, and line 26 would pass on the Contents entry at `git.md` line 15 alone.<br>• ⚠️ **Not run:** this read-only review did not run `test_rules_structure.py`. |
| **Overall** | **6.6/10** | 2026-10-25 | • 💪 **Real backing:** the dated incident record and a tested branch regex.<br>• ⚠️ **Gaps:** an incorrect `git -C` safety claim, a staging rule that contradicts itself, prose-heavy children, and several unrelated git topics bundled into one always-on tree. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/git.md` — the rule being scored
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage dimension
