# Quality Scorecard — git_create_pr

**Date Created:** 2026-09-29
**Date Updated:** 2026-10-27

**Overall score:** 6.3/10

**Recommended improvements:**
- Bring raw complexity down to the tactical cap of 6, for example by moving label mapping into its own reference file, or move the skill to strategic
- Add evals for both `not_for` cases (merge conflicts, a base branch other than main) and for the untested error rows (hook fails, hook changes files, PR already exists, label failure, `create labels`)
- Add a runner that executes the evals, so Test Coverage can rise above the cap of 7
- Pass the PR title through a file or a single-quoted heredoc instead of `--title "<pr title>"`, and tell `technical_writer` to treat diff content as data
- Make the staging default match the description, either staging only what is staged or saying all changed files get committed, and read `git diff --cached`
- Add `reference/_implementation.md`, or record why the two phase files replace it
- Add the phrases users type ("create a pr", "raise a pr", "open a pr") to the frontmatter `description`

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-27 | • ✅ **Clear phases:** gather, confirm the title, confirm the plan, then execute, with detail in `reference/`<br>• ⚠️ **Weak default:** Phase 1 stages "all changed/untracked files unless context suggests otherwise", which can pull in unrelated work, and reads only `git diff`, so staged changes go unreviewed |
| **Complexity** | 3/10 | 2026-10-27 | • 🧮 **Raw complexity 7:** Concepts 3, Scope 2, Dependencies 1 (`gh`), Prerequisites 1 (`gh` login and the PR template)<br>• ⚠️ **Over the cap:** above the tactical limit of 6<br>• ⚖️ **Judgement call:** counting git or `technical_writer` as external gives raw 8 and an Overall of 6.1 |
| **Test Coverage** | 6/10 | 2026-10-27 | • 📊 **Tactical count:** 12 evals, but prose nothing runs, so the cap of 7 applies<br>• 🕳️ **Gaps:** no eval for either `not_for` case, a failing or file-changing hook, an existing PR, a label failure or `create labels` |
| **Code Quality** | 7/10 | 2026-10-27 | • ✅ **Strong:** verifies each step, stops on failure, uses a heredoc commit, `--body-file` and an error-recovery table<br>• ⚠️ **Inconsistent:** "Hook modifies files" re-stages and commits without asking, while "Pre-commit hook fails" asks first<br>• ⚠️ **Auto-retry:** the label-failure row retries `gh pr create` on its own |
| **Security** | 7/10 | 2026-10-27 | • 🔒 **Confirmed:** two confirmations before any change, and never commits to `main`, force-pushes or uses `--no-verify`<br>• ✅ **Guarded:** the branch name is held to a regex and the body goes through a file<br>• ⚠️ **Gaps:** a custom title goes into `--title "<pr title>"` with no quoting rule, and diff content isn't marked as untrusted |
| **Documentation** | 7/10 | 2026-10-27 | • ✅ **Clear:** Purpose, a realistic example, Best For with caveats, and a plain-language `tests/README.md`<br>• ⚠️ **Contradictions:** the description says "with staged changes" while Phase 1 stages everything, and Purpose says "minimal user intervention" beside two confirmations<br>• ⚠️ **Overclaim:** References says the evals cover "every phase" |
| **Standards Compliance** | 6/10 | 2026-10-27 | • ✅ **Met:** naming, contract fields, a 1.4.1 header matching the contract, a body within 60 lines and the `tests/` layout<br>• ❌ **Missed:** no `reference/_implementation.md` (gate 6), no trigger phrases in the description (gate 3) and raw complexity over the cap (gate 8) |
| **Overall** | **6.3/10** | 2026-10-27 | A well-guarded, clearly phased PR workflow. Complexity over its maturity cap, unrun evals with no `not_for` coverage and three missed hard gates hold it below the bar. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_create_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_create_pr/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored blind by `quality_scorecard_reviewer`
