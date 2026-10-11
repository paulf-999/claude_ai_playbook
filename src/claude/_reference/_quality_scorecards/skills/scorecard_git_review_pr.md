# Quality Scorecard — git_review_pr

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-06

**Overall score:** 8.7/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 9/10 | 2026-10-06 | • ✅ **Split:** the skill fetches and posts, while the `code_reviewer` agent does the analysis<br>• ✅ **Options:** a `--dry-run`, and an update to your earlier review instead of a duplicate |
| **Complexity** | 6/10 | 2026-10-06 | • 🧮 **Raw complexity 4:** review plus large-diff split, secret check, dry run and update (Concepts 2), one PR (Scope 1), `gh` (Dependencies 1), no fixtures |
| **Test Coverage** | 8/10 | 2026-10-06 | • 📊 **Count:** 8 evals, the draft maximum, covering every new path<br>• ⚠️ **Gaps:** no scenario for complexity scoring or a declined post, and nothing runs the evals |
| **Code Quality** | 9/10 | 2026-10-06 | • ✅ **Large diffs:** whole files up to a 500-line budget, with the rest summarised by file<br>• ✅ **Errors:** stops on no PR or an empty diff, and keeps the draft if posting fails |
| **Security** | 10/10 | 2026-10-06 | • 🔒 **Untrusted input:** PR content is passed as data, and planted instructions are flagged<br>• 🔒 **Secret check:** blocks posting a comment that quotes a key, token or password, tested against sample secrets |
| **Documentation** | 10/10 | 2026-10-06 | • ✅ **SKILL.md:** a real example run, caveats and the reasons for its limits<br>• ✅ **Reference:** phases, troubleshooting table and FAQ |
| **Standards Compliance** | 9/10 | 2026-10-06 | • ✅ **Hard gates:** contract, six-section SKILL.md, full trigger variants, `tests/` with README, and both reference files<br>• ⚠️ **Tested:** no behavioural pytest, so `tested` is false |
| **Overall** | **8.7/10** | 2026-10-06 | A safe, well-documented draft-stage skill whose added options cost some simplicity, held back by unrun evals and no usage record. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_review_pr/tests/evals.yaml` — Test Coverage dimension
