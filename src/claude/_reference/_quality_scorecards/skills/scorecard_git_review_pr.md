# Quality Scorecard — git_review_pr

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-26

**Overall score:** 7.6/10

**Recommended improvements:**
- Add a runner for `tests/evals.yaml` (#387), so Test Coverage can rise above the cap for unrun scenarios
- Add scenarios for the 4 untested "not for" hand-offs: creating a PR, a formal review, editing the PR's code and a bug hunt
- Lower complexity further, for example by moving the update-earlier-review branch or the large-diff budget into helpers
- Record use-frequency evidence for the strategic claim, which `_core_standards.md` asks for
- Set `output.type` in the contract to a value `_core_standards.md` allows, instead of `mixed`

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-26 | • ✅ **Clear order:** seven phases, with the detail in `reference/`<br>• 📐 **Not one job each:** Phase 5 checks, saves and handles the dry-run exit, and a flagged secret loops back to Phase 4 |
| **Complexity** | 5/10 | 2026-10-26 | • 🧮 **Raw complexity 5:** Concepts 2, Scope 1, Dependencies 1 (`gh`), Prerequisites 1 (`gh` login), within the strategic limit of 8<br>• 🔀 **Branching:** dry-run, the amend loop, the secret-check loop-back, update or new comment, and the 500-line budget |
| **Test Coverage** | 7/10 | 2026-10-26 | • 📊 **Strategic count, unrun:** 12 scenarios including adversarial ones, capped at 7 because nothing runs them<br>• 🧪 **One runnable test:** the pytest checks the secret pattern and its flags<br>• 🕳️ **Gap:** only 1 of the 5 `not_for` cases has a scenario |
| **Code Quality** | 8/10 | 2026-10-26 | • ✅ **Strong:** argument allow-list, empty-diff and no-PR stops, `mktemp`, `--body-file` and failed-post handling<br>• 🔧 **Fixed in the same PR:** the secret check's pass or fail rule was undefined, since `\| cut` always exits 0, so `set -o pipefail` and an exit-status rule now cover it |
| **Security** | 9/10 | 2026-10-26 | • 🛡️ **Defended:** explicit `y` before posting, untrusted PR content, input checked before any shell call, the secret check before saving with line numbers only, and no formal approval<br>• 🔍 **Known gap:** JWTs and connection strings get through, which Known gaps records with a workaround |
| **Documentation** | 8/10 | 2026-10-26 | • ✅ **Complete:** purpose, a seven-phase example, caveats, Known gaps with workarounds, troubleshooting and FAQ<br>• 🔧 **Fixed in the same PR:** `tests/README.md` still said "tactical", and Best For said "tested" where the scenarios are unrun |
| **Standards Compliance** | 8/10 | 2026-10-26 | • ✅ **Met:** name, a 2.0.0 header matching the contract, instructions, body length, `tests/` layout and reference files<br>• ❌ **Contract value:** `output.type: mixed` isn't an allowed value, which predates this change<br>• ⚠️ **Evidence:** no file records the use frequency behind the strategic claim, which the owner confirmed on 2026-10-26<br>• 🔧 **Fixed in the same PR:** `test_coverage_level` went back to `basic` |
| **Overall** | **7.6/10** | 2026-10-26 | Safe, well-defended and well-documented, held back by moderate complexity, scenarios nothing runs and a strategic claim with no usage record. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_review_pr/reference/_implementation.md` — Design, Code Quality and Security dimensions
- `src/claude/skills/_git_skills/git_review_pr/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 5, scored blind by `quality_scorecard_reviewer`
