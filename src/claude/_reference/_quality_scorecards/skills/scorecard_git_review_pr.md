# Quality Scorecard — git_review_pr

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-26

**Overall score:** 7.6/10

**Recommended improvements:**
- Record the raw complexity sum, and bring it below the tactical limit of 6, for example by splitting off the post-or-update step or the large-diff budget
- Add scenarios for the 4 untested "not for" cases, or a runner that proves the routing, to lift Test Coverage above the unrun cap
- Split Phase 5 into "check and save" and "confirm", and say which phase a flagged-secret retry returns to
- Make `tested:` and `test_coverage_level` match the secret-check pytest that exists
- Check that the PR is still open before analysis

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-26 | • ✅ **Clear order:** six phases, with the detail in `reference/`<br>• 📐 **Busy phase:** Phase 5 runs the secret check, saves, stops for a dry run and confirms<br>• 🔁 **Open retry:** after a flagged secret, it doesn't say which phase to go back to |
| **Complexity** | 4/10 | 2026-10-26 | • 🧮 **Raw complexity 6:** Concepts 3, Scope 0, Dependencies 2 (`gh` and the `code_reviewer` agent), Prerequisites 1 (`gh` login and an open PR)<br>• ⚠️ **At the ceiling:** 6 is the tactical limit, and no file records the calculation |
| **Test Coverage** | 7/10 | 2026-10-26 | • 📊 **Right count, unrun:** 12 prose scenarios cover happy paths, errors, edge cases and adversarial input, capped at 7 because nothing runs them<br>• 🧪 **One runnable test:** `test_git_review_pr_secret_check.py` runs the doc's own pattern<br>• 🕳️ **Gap:** 4 of the 5 `not_for` cases have no scenario |
| **Code Quality** | 8/10 | 2026-10-26 | • ✅ **Handled:** a strict argument pattern, a failed login, no PR, an empty diff and a failed post<br>• ✅ **Safe writes:** `mktemp` then a move, and posting with `--body-file`<br>• ⚠️ **Gaps:** no check that the PR is still open, and no limit on secret-check retries |
| **Security** | 9/10 | 2026-10-26 | • 🛡️ **Defended:** an explicit `y` before posting, PR content treated as untrusted, input checked against a pattern before any shell call, and no formal review<br>• 🔒 **Secret check:** runs before saving, prints only line numbers and is tested<br>• 🔍 **Heuristic:** it only catches known shapes, so a JWT or an Azure connection string would get through |
| **Documentation** | 9/10 | 2026-10-26 | • ✅ **Complete set:** purpose, a six-phase example, troubleshooting, FAQ and caveats<br>• ⚠️ **Mismatch:** `tested: false` sits beside an existing skill test, with no reason given |
| **Standards Compliance** | 8/10 | 2026-10-26 | • ✅ **Most gates met:** name, contract, `not_for`, a matching 1.1.0 version, `tests/` layout, README, reference files and body length<br>• ❌ **Complexity unrecorded (gate 8):** no file gives the calculation, and the skill sits at the limit<br>• ⚠️ **Tags:** `tested: false` and `test_coverage_level: basic` don't match the existing test |
| **Overall** | **7.6/10** | 2026-10-26 | A safe, well-documented tactical skill held back by complexity at the ceiling with no recorded calculation, and by prose evals that leave four "not for" hand-offs untested. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_review_pr/reference/_implementation.md` — Design, Code Quality and Security dimensions
- `src/claude/skills/_git_skills/git_review_pr/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 4, scored blind by `quality_scorecard_reviewer`
