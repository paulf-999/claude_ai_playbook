# Quality Scorecard — git_review_pr

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-25

**Overall score:** 7.1/10

**Recommended improvements:**
- Add scenarios for the 4 untested "not for" cases (creating a PR, a formal review, editing the PR's code and a bug hunt) and for a declined post
- Write the exact pattern for accepted arguments into Phase 1 and the Instructions, including the owner and repo parts of a PR URL
- Resolve the drafts path from the config directory instead of hardcoding `~/claude/`
- Bring raw complexity below the tactical limit of 6, for example by splitting Phase 4 into amend and secure-save-confirm

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-25 | • ✅ **Clean split:** five clear phases, with the procedure in `reference/`<br>• 📐 **Overloaded phase:** Phase 4 still shows, amends, checks for secrets, saves, handles dry-run and confirms<br>• 🔁 **Repetition:** the SKILL.md Instructions repeat parts of that procedure |
| **Complexity** | 4/10 | 2026-10-25 | • 🧮 **Raw complexity 6:** Concepts 3, Scope 1 (`_drafts/` plus a temp file), Dependencies 1 (`gh`), Prerequisites 1 (`gh` login)<br>• ⚠️ **At the ceiling:** 6 is the most a tactical skill may have |
| **Test Coverage** | 6/10 | 2026-10-25 | • 📊 **Right count, unrun:** 12 prose scenarios, the tactical count, but nothing runs them, which caps this at 7<br>• ⚠️ **One "not for" case:** only `local_diff_routed_to_code_reviewer` covers a `not_for` entry<br>• 🧪 **One runnable test:** `test_git_review_pr_secret_check.py` covers only the secret pattern |
| **Code Quality** | 8/10 | 2026-10-25 | • ✅ **Handled:** a failed login, no PR, an empty diff, a failed post (draft kept) and 403 or 404 errors<br>• ✅ **Safe save:** writes a temporary file and moves it once the check passes<br>• ⚠️ **Loose validation:** Phase 1 says "anything else is rejected" but gives no exact pattern |
| **Security** | 8/10 | 2026-10-25 | • 🛡️ **Defended:** an explicit `y` before posting, PR content treated as untrusted, the secret check before saving and only line numbers shown<br>• ⚠️ **Unconstrained URL:** the owner and repo parts of an accepted PR URL aren't limited before they reach `gh`<br>• 🔍 **Heuristic:** the secret pattern is a list of known formats, so new ones can slip through |
| **Documentation** | 9/10 | 2026-10-25 | • ✅ **Complete set:** purpose, a realistic example, caveats, reasons for the limits, troubleshooting and FAQ<br>• 🕳️ **Minor gaps:** the example shows no dry run, and `tested: false` sits beside an existing pytest without explanation |
| **Standards Compliance** | 7/10 | 2026-10-25 | • ✅ **Most gates met:** naming, contract, `tests/` layout, README, reference files and a 52-line body<br>• ❌ **Hardcoded path (gate 9):** the Instructions write `~/claude/_drafts/general/...`, against `portable_paths.md`<br>• ⚠️ **Reviewer error:** it also flagged an unbumped version, but #391 raised it from 0.5.1 to 1.0.0 in the same edit, so that finding doesn't stand |
| **Overall** | **7.1/10** | 2026-10-25 | A sound, well-defended tactical skill held back by unrun evals with few "not for" cases, complexity at the ceiling and a hardcoded drafts path. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_review_pr/reference/_implementation.md` — Design, Code Quality and Security dimensions
- `src/claude/skills/_git_skills/git_review_pr/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 3, scored by `quality_scorecard_reviewer`
