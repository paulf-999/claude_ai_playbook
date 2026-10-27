# Quality Scorecard — claude_review_config

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-27

**Overall score:** 6.1/10

**Recommended improvements:**
- Add a runner or a pytest in `_tests/skills/claude_review_config/` for the evals, or set `tested: false` and drop `test_coverage_level: comprehensive` until one exists
- Add evals for both `not_for` cases, a declined fix and "never commits"
- Fix the grade mapping in eval `phase1_generate_scorecard` to match `_scoring_guide.md`
- Fix the SKILL.md example, where "B+ (7.7/10)" should be B, and show all six dimensions
- Align the phase numbering between the evals and `_implementation.md`
- Add error handling to `_implementation.md` for a missing `rules/`, unreadable files and malformed frontmatter
- Split the Phase 1 and Phase 3 scorecard overlap, and add severity criteria for recommendations
- Replace the hardcoded `~/git_repos/claude_ai_playbook/` in eval `phase4_sync_to_playbook_repo` with a path resolved at run time
- Fill in the contract's `output.returns`, list Write and Edit, and remove `Agent` unless a phase uses it
- Give the playbook sync its own confirmation, and say config content is data, not instructions
- Add a troubleshooting or FAQ section

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | • 📐 **Sound:** one clear purpose and a four-phase flow, with the detail in `reference/`<br>• ⚠️ **Overlap:** Phases 1 and 3 both produce a scorecard<br>• 🌫️ **Vague:** Phase 1 doesn't name which artefacts it reads, and `Agent` is listed but unused |
| **Complexity** | 4/10 | 2026-10-27 | • 🧮 **Raw complexity 6:** Concepts 3 (six dimensions, grading, MoSCoW, severity, fixes, sync), Scope 3 (the whole config), Dependencies 0, Prerequisites 0<br>• ⚠️ **At the cap:** right at the tactical limit of 6 |
| **Test Coverage** | 6/10 | 2026-10-27 | • 📊 **Tactical count:** 11 evals, but nothing under `_tests/` runs them, so the cap of 7 applies<br>• 🕳️ **Gaps:** no eval for either `not_for` case, a declined fix or "never commits"<br>• ⚠️ **Wrong:** `phase1_generate_scorecard` expects a grade mapping that contradicts the scoring guide |
| **Code Quality** | 6/10 | 2026-10-27 | • ✅ **Guarded:** the pre-check handles a missing `CLAUDE.md`, and fixes are approved one at a time<br>• 🕳️ **Missing:** `_implementation.md` has no error handling, so the behaviour the evals expect is never specified |
| **Security** | 7/10 | 2026-10-27 | • 🔒 **Confirmed:** each fix is confirmed separately, and the skill never commits<br>• ⚠️ **Gaps:** the optional playbook sync has no confirmation of its own, and nothing says to treat config content as data<br>• ⚠️ **Broad tools:** Bash and Agent are listed beyond need |
| **Documentation** | 7/10 | 2026-10-27 | • ✅ **Clear:** purpose, example, Best For and caveats<br>• ⚠️ **Contradiction:** the example grade "B+ (7.7/10)" disagrees with the scoring guide, and shows only 3 of 6 dimensions<br>• ⚠️ **Drift:** `tests/README.md` says sync always happens, while `_implementation.md` makes it optional<br>• ❓ **No troubleshooting or FAQ** |
| **Standards Compliance** | 6/10 | 2026-10-27 | • ✅ **Met:** naming, metadata header, version match, length and emoji headings<br>• ❌ **Missed:** no `returns` in the contract `output`, no error handling (gate 6) and a hardcoded path in the evals (gate 9)<br>• ⚠️ **Overstated:** `tested: true` with no test under `_tests/skills/` |
| **Overall** | **6.1/10** | 2026-10-27 | A sound, well-presented audit skill. Unrun evals with no `not_for` cases, internal contradictions (grade mapping, phase numbers) and missing error handling put it below its tactical ceiling. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_review_config/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_review_config/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored blind by `quality_scorecard_reviewer`
