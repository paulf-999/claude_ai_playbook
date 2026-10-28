# Quality Scorecard — technical_writer

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-28

**Overall score:** 6.3/10

**Recommended improvements:**
- Decide whether this agent drafts Confluence pages, then make the description, "When to use", triggers and evals all say the same thing.
- If Confluence drafting stays, add `confluence_create_page`'s own drafting to "Not for", or remove Confluence pages from the agent.
- Add triggers for common phrasings such as "write a PR description" and "write the PR body".
- Record real uses, for example usage rows or dated PRs drafted by the agent, or step maturity down to draft as line 59 says to.
- Fix or explain the 4 failing runnable evals, and add `run` blocks to the 5 output evals that have none.
- Make the `pr_body_links_jira_ticket` setup branch match its run prompt branch.
- Add a "why" to each Constraint, change the `~/.claude/` References to `~/claude/`, and trim the file to about 60 lines.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-28 | • ✅ **Description:** for PR bodies, the description says what the agent does, when to use it and when not to<br>• 🔀 **Contradiction:** line 3 sends new Confluence pages to `confluence_create_page`, but line 25 ("Drafts PR/MR descriptions and Confluence page text") and line 30 list Confluence pages as in scope<br>• 🔍 **Triggers:** only `"draft pr body"` and `"draft pr description"` are listed, so the description's own "write a PR body" phrasing and audience rewrites have no trigger |
| **Scope Boundaries** | 6/10 | 2026-10-28 | • ✅ **Fenced:** "Not for" names the publishing skills, ADRs, runbooks, READMEs, diagrams and edits to existing docs<br>• 🔁 **Overlap:** line 3 says `confluence_create_page` "applies this agent's writing approach", so both share the Confluence-drafting job, and "Not for" only fences off publishing (line 32) |
| **Complexity** | 6/10 | 2026-10-28 | • 🧮 **Raw 4:** Concepts 2 (PR bodies, Confluence pages, audience rewrites, decline and hand-off), Scope 1 (repo template in, two drafts folders out), Dependencies 0, Prerequisites 1 (a PR template must exist)<br>• ✅ **No services:** no external integration is needed |
| **Evidence of Need** | 5/10 | 2026-10-26 | • ❓ **No record:** line 58 says "neither `git_create_pr` nor `confluence_create_page` calls it yet, and no usage record exists"<br>• 📝 **Plausible job:** PR descriptions are a real recurring task, but no file shows this agent being used for one |
| **Test Coverage** | 5/10 | 2026-10-28 | • 📊 **Count met:** 12 evals, at the top of the tactical range of 8-12, and they include the "not for" cases<br>• ❌ **Runner fails:** `audit_agent_evals.py` passed 3 of 7 runnable evals (43%), which is below 75%, so the cap of 7 applies<br>• ❌ **Boundaries fail:** all three runnable boundary evals failed (`hands_off_publishing_to_skill`, `declines_adr`, `declines_editing_existing_docs`), and so did `confluence_asks_for_audience`<br>• ⚠️ **Unrun output evals:** 5 audience and tone evals (e.g. `confluence_mixed_audience`, `tone_differs_by_audience`) have no `run` block, and they test output rather than routing<br>• 🐛 **Inconsistent eval:** in `pr_body_links_jira_ticket`, the setup branch is `feature/proj_1234_retry_backoff` but the run prompt uses `feature/PROJ-1234_add_retry` |
| **Structural Compliance** | 7/10 | 2026-10-26 | • ✅ **Present:** all frontmatter fields, the metadata header and every required section are there, with 7 principles<br>• 📏 **Length:** 66 lines, longer than the ~40-60 the checklist asks for<br>• ⚠️ **No rationale:** the Constraints give no "why" (e.g. line 52, "Out of scope: Does NOT edit existing docs…"), and the checklist requires one<br>• ⚠️ **Maturity unsupported:** it is tactical with `tested: true` while 4 runnable evals fail and no use is recorded<br>• 🔗 **Path:** References lines 64-65 use `~/.claude/rules/…`, but the live config lives at `~/claude/` |
| **Tool Safety** | 9/10 | 2026-10-26 | • 🔒 **Least privilege:** only `Read, Grep, Glob, Write` are allowed, and Write is needed for the drafts<br>• ✅ **Isolated:** `isolation: worktree` with `model: inherit`<br>• 📝 **Prose-only limit:** the drafts-folder restriction (line 49) relies on the instruction alone, because the agent writes to `~/_drafts/`, which is outside the worktree |
| **Overall** | **6.3/10** | 2026-10-28 | • 💪 **Safe and lean:** tightly scoped tools, worktree isolation and a clear PR-template workflow<br>• ⚠️ **Unproven:** the runner fails all of its boundary cases, the Confluence scope contradicts itself and no use is recorded |

## 🔗 Related files

- `src/claude/agents/core/technical_writer/AGENT.md` — the artefact being scored
- `src/claude/agents/core/technical_writer/evals.yaml` — Test Coverage and Structural Compliance
- `src/claude/scripts/_audit_scripts/audit_agent_evals.py` — Test Coverage (run pass rate)
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
