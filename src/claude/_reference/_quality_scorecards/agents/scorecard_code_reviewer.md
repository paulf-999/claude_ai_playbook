# Quality Scorecard — code_reviewer

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-26

**Overall score:** 8.0/10

**Recommended improvements:**
- Make `clean_change_approved` check for a plain Approve with no Must or Should items, not just the word "approve"
- Make `declines_to_edit_or_post` check that the agent declines to edit, not only that it names `git_review_pr`
- Catch alignment findings in `skips_linter_style` even when they lack a bold severity label
- Add the "bug hunt goes to `/code-review`" boundary and a "review this PR" trigger to the description

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-26 | • 🔍 **Description:** says what it does, when to use it, and its six themes<br>• ⚠️ **No "when not":** line 3 omits the "bug hunt goes to `/code-review`" boundary, which sits only at line 35<br>• ⚠️ **Missing trigger:** lines 9–14 miss "review this PR", even though the description uses it |
| **Scope Boundaries** | 8/10 | 2026-10-26 | • ✅ **Named neighbours:** "not for" names `git_review_pr` and `/code-review` (lines 34–35)<br>• ⚠️ **Unnamed neighbour:** line 51 says whole-repo audits are separate but doesn't name `claude_review_config` |
| **Complexity** | 7/10 | 2026-10-26 | • 🧮 **Raw complexity 3:** one job with no external services, reading rules and style guides from several folders (lines 39, 51), across about 6 behaviours (lines 41–46, 52) |
| **Evidence of Need** | 7/10 | 2026-10-26 | • ✅ **One real use:** line 57 records reviewing an infrastructure PR through `git_review_pr` on 2026-10-05<br>• ⚠️ **No second use:** no file records repeat use, and eval runs don't count |
| **Test Coverage** | 8/10 | 2026-10-26 | • 📊 **Runs:** 6 of 8 evals run, the 2 skipped need a full session, and the clean run on 2026-10-26 passed 6/6<br>• ⚠️ **Weak check:** `clean_change_approved` matches only `(?i)approve` (lines 69–72), which also passes "Approve with suggestions", and nothing checks for Should items<br>• ⚠️ **Weak check:** `declines_to_edit_or_post` only checks that `git_review_pr` is named (lines 226–227)<br>• ⚠️ **Gap from a fix:** `skips_linter_style` (line 200) misses an alignment finding written without a bold severity label |
| **Structural Compliance** | 8/10 | 2026-10-26 | • ✅ **Hard gates:** frontmatter, metadata header, all sections, 6 principles, constraints with reasons, maturity justified, every eval field present<br>• ⚠️ **Length:** 65 lines, past the ~40–60 target<br>• ⚠️ **Hardcoded path:** line 64 uses a literal `~/.claude/rules/...` |
| **Tool Safety** | 10/10 | 2026-10-26 | • 🔒 **Allowlist:** `Read, Grep, Glob` (line 15), with no Bash, Write or MCP<br>• ✅ **Isolation:** line 53 explains why `none` is safe ("it never writes files") |
| **Overall** | **8.0/10** | 2026-10-26 | • 💪 **Strength:** a tight read-only allowlist, a real recorded use, and runnable evals that pass<br>• ⚠️ **Gap:** three eval checks weaker than the assertions they stand for |

## 🔗 Related files

- `src/claude/agents/core/code_reviewer/AGENT.md` — the agent being scored
- `src/claude/agents/core/code_reviewer/evals.yaml` — Test Coverage dimension
- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — Scope Boundaries dimension
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance dimension
