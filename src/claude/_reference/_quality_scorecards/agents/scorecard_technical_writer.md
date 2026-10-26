# Quality Scorecard — technical_writer

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-26

**Overall score:** 7.3/10

**Recommended improvements:**
- Resolve line 3's hand-off of Confluence pages to `confluence_create_page` against lines 25 and 30, which say the agent drafts them
- Record real uses, or lower the Tactical maturity on line 4 until usage exists
- Give the boundaries on line 52 a reason, and say how audience rewrites differ from editing existing docs
- Check the draft path and "no draft written" assertions, which the run blocks don't cover

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-26 | • 🔍 **Description:** says what the agent does, when to use it and when not to<br>• ⚠️ **Confluence contradiction:** line 3 sends new Confluence pages to `confluence_create_page`, but lines 25 and 30 say the agent drafts Confluence page text itself<br>• ⚠️ **Narrow triggers:** lines 10–12 miss common phrasings such as "write a PR description" |
| **Scope Boundaries** | 7/10 | 2026-10-26 | • ✅ **Named neighbours:** the "not for" list names `git_create_pr` and `confluence_create_page`<br>• ⚠️ **Shared job:** Confluence drafting is claimed both here (line 30) and by `confluence_create_page` (line 3)<br>• ⚠️ **Fuzzy edge:** line 31's "audience rewrites" never says how they differ from line 33's excluded "editing existing docs" |
| **Complexity** | 7/10 | 2026-10-26 | • 🧮 **Raw complexity 3:** three jobs in one agent (lines 29–31), reads `.github/` and writes a drafts folder, and the PR path depends on a template existing (line 45) |
| **Evidence of Need** | 5/10 | 2026-10-26 | • ❓ **No usage:** line 58 says "neither `git_create_pr` nor `confluence_create_page` calls it yet, and no usage record exists"<br>• ⚠️ **Maturity unsupported:** that is weak support for Tactical maturity on line 4 |
| **Test Coverage** | 8/10 | 2026-10-26 | • 📊 **Runs:** 7 of 12 evals run, and the clean run on 2026-10-26 passed 7/7, with the "not for" cases covered by `declines_adr` and `declines_editing_existing_docs`<br>• ⚠️ **Core checks skipped:** the 5 skipped evals are core output checks, not routing (evals.yaml lines 107–189), so the 90% guidance stops at 8<br>• ⚠️ **Assertions unchecked:** the run blocks never check the absolute draft path (line 26) or "No draft file is written" (lines 96, 144, 217) |
| **Structural Compliance** | 7/10 | 2026-10-26 | • ✅ **Basics met:** complete frontmatter, metadata header, every section, 7 principles, every eval field present<br>• ⚠️ **Length:** 66 lines against the ~40–60 target<br>• ⚠️ **No reasons:** line 52's "Out of scope" gives no why<br>• ⚠️ **Maturity case:** lines 57–59 cite eval count only, with no frequency of use |
| **Tool Safety** | 9/10 | 2026-10-26 | • 🔒 **Allowlist:** `Read, Grep, Glob, Write` (line 13) is least privilege for drafting, with no Bash or MCP<br>• ⚠️ **Isolation gap:** `isolation: worktree` (line 15) doesn't contain drafts written to a home-directory path (line 49) |
| **Overall** | **7.3/10** | 2026-10-26 | • 💪 **Strength:** a least-privilege allowlist, and its runnable evals all pass<br>• ⚠️ **Gap:** no recorded use behind Tactical maturity, a Confluence job claimed twice, and core output checks that don't run |

## 🔗 Related files

- `src/claude/agents/core/technical_writer/AGENT.md` — the agent being scored
- `src/claude/agents/core/technical_writer/evals.yaml` — Test Coverage dimension
- `src/claude/skills/_git_skills/git_create_pr/SKILL.md` — Scope Boundaries dimension
- `src/claude/skills/_atlassian_skills/confluence_create_page/SKILL.md` — Scope Boundaries dimension
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance dimension
