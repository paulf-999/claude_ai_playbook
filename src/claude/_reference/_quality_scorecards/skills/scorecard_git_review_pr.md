# Quality Scorecard — git_review_pr

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-22

**Overall score:** 7.1/10

**Recommended improvements:**
- Add "not for" scenarios to `tests/evals.yaml`, plus an invalid-argument case and an empty-diff case
- Run the secret check before saving the draft, so a flagged secret never lands in `_drafts/`
- Resolve the drafts path from the config directory instead of hardcoding `~/claude/`
- Bring raw complexity to 4 or below, for example by splitting Phase 4 into review-and-amend and check-and-post

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 8/10 | 2026-10-22 | • ✅ **Clean split:** SKILL.md holds only instructions, with the five phases in `reference/_implementation.md` and the template in `reference/_formats.md`<br>• 📐 **Overloaded phase:** Phase 4 shows the comment, runs the amendment loop, saves the draft, runs the secret check, handles dry-run and asks for confirmation |
| **Complexity** | 5/10 | 2026-10-22 | • 🧮 **Raw complexity 5:** 6+ concepts (Concepts 3), `gh` (Dependencies 1), `gh` login (Prerequisites 1), one skill folder (Scope 0)<br>• 🔀 **Branching:** Phase 4 branches on verdict, amend selection, secret-check result, `--dry-run` and the y/n reply, and Phase 5 adds update-or-new |
| **Test Coverage** | 6/10 | 2026-10-22 | • 📊 **Right count, unrun:** 8 prose scenarios in `tests/evals.yaml`, within the draft range, but nothing runs them<br>• ⚠️ **No "not for" case:** none of the 5 `not_for` entries in `skill.contract.yaml` has a scenario<br>• 🕳️ **Known gaps:** no scenario for a declined post, an invalid argument or an empty diff |
| **Code Quality** | 8/10 | 2026-10-22 | • ✅ **Validation:** PR arguments are limited to digits or a GitHub pull URL, and no-PR, empty-diff and failed-post cases are handled<br>• ⚠️ **Unhandled failures:** `reference/_implementation.md` doesn't cover a failed `gh pr diff`, a failed `code_reviewer` call or a malformed template |
| **Security** | 8/10 | 2026-10-22 | • 🛡️ **Defended:** an explicit `y` before posting, PR content treated as untrusted data, shell input limited to a number or URL, and a secret check<br>• ⚠️ **Secret saved first:** in Phase 4, "Save" runs before "Secret check", so a flagged secret stays in plain text in `_drafts/`<br>• 🔍 **Narrow pattern:** the `grep -nE` pattern misses other providers' tokens and quoted values |
| **Documentation** | 8/10 | 2026-10-22 | • ✅ **Complete set:** a worked example in SKILL.md, and a troubleshooting table and FAQ in `reference/_implementation.md`<br>• 🕳️ **Missing rows:** no troubleshooting row for a failed `code_reviewer` call or a secret-check false positive<br>• 🔀 **Path drift:** SKILL.md line 22 writes `~/claude/_drafts/general/...`, while `reference/_implementation.md` writes `$HOME/claude/_drafts/general/...` |
| **Standards Compliance** | 7/10 | 2026-10-22 | • ✅ **Most gates met:** name, contract, frontmatter, metadata header, headings, length, `tests/` layout and reference files<br>• ❌ **Hardcoded path (gate 9):** the drafts path assumes the config folder's name, against `portable_paths.md`<br>• ❌ **Complexity cap (gate 8):** raw complexity 5 is above the draft limit of 4 |
| **Overall** | **7.1/10** | 2026-10-22 | A well-structured, safety-conscious draft held back by unrun evals with no "not for" cases, complexity above the draft cap and a hardcoded draft path. |

## 🔗 Related files

- `src/claude/skills/_git_skills/git_review_pr/SKILL.md` — the skill being scored
- `src/claude/skills/_git_skills/git_review_pr/reference/_implementation.md` — Design, Code Quality and Security dimensions
- `src/claude/skills/_git_skills/git_review_pr/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored by `quality_scorecard_reviewer`
