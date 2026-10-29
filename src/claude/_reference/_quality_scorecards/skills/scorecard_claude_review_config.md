# Quality Scorecard — claude_review_config

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-29

**Overall score:** 6.1/10

**Recommended improvements:**
- Fix the grade in SKILL.md's Example Usage: 7.7/10 should be B, not B+, under `reference/_scoring_guide.md` (7.5–7.9 = B).
- Add an error-handling section to `reference/_implementation.md` for a missing `rules/` folder and malformed YAML, so the two error evals test documented behaviour.
- Renumber the evals to match `_implementation.md`, where Phase 3 is the report and Phase 4 is offering fixes.
- Make the MoSCoW scope match: `phase2_moscow_table` expects "Must/Should only", but `_implementation.md` lists Must, Should, Could and Won't.
- Add a runner or a pytest for the evals, or keep `tested: false` and drop `test_coverage_level: comprehensive` until one exists.
- Add a "not for" eval for "reviewing playbook repo structure", and an eval where the user turns a proposed fix down.
- List Write and Edit in the contract's tools, give a reason for Bash and Agent or remove them, and put a confirm step on the playbook sync as its own action.
- Change "11 test scenarios" to 12 in SKILL.md References and in the `evals.yaml` description.
- Add "review", "score" and "health check" to the frontmatter description so it matches the contract's triggers.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | Four clear phases, with the detail kept in `reference/`. But a scorecard is the output of both Phase 1 ("Scorecard with per-dimension scores") and Phase 3. Phase 4 also does two jobs: it applies fixes and it syncs to the playbook. |
| **Complexity** | 4/10 | 2026-10-27 | Raw sum is 6: Concepts 2 (score, gaps, report, fix/sync), Scope 3 (scans the whole config), Dependencies 0, Prerequisites 1 (needs a config folder). That is 10 − 6 = 4, and it sits right at the tactical limit of 6. |
| **Test Coverage** | 6/10 | 2026-10-27 | 12 evals is right for tactical, but they are prose that nothing runs (no runner, nothing under `_tests/`, and `tested: false`), so the cap is 7. Only one of the two `not_for` items has an eval, and the playbook-repo case has none. The evals' phase labels ("Phase 3: Offer Fixes", "Phase 4: Apply Fixes") don't match `_implementation.md`. `phase2_moscow_table` says "Must/Should only", which contradicts the four MoSCoW rows in the implementation. |
| **Code Quality** | 6/10 | 2026-10-27 | There is no code. The CLAUDE.md pre-check and the `~` expansion are stated. But `_implementation.md` has no error handling, even though `error_malformed_yaml_in_rules` and `error_missing_rules_directory` expect a graceful exit. The worked example also maps 7.7 to "B+", which contradicts the scoring guide. |
| **Security** | 7/10 | 2026-10-27 | It asks for confirmation before each fix (`confirmation_required: true`, "Never: apply a fix the user hasn't approved individually"), and it never commits. But Phase 4 step 4 "Optionally sync to the playbook repo" writes to a second location without its own confirm step. The contract lists Bash and Agent with no reason, and nothing says to treat the content of the config files it reads as data. |
| **Documentation** | 6/10 | 2026-10-29 | The Purpose, the Best For caveats, the maturity justification and the plain-language `tests/README.md` are clear. But the example's grade is wrong, and SKILL.md and the `evals.yaml` description both say "11 test scenarios" when there are 12. There is no troubleshooting section for the error cases. |
| **Standards Compliance** | 7/10 | 2026-10-29 | Naming, the six sections, the metadata header (1.1.4 in both SKILL.md and the contract), the length and the heading emojis all pass. Gaps: `_implementation.md` has no error handling (hard gate 6). The contract's tools sit under `dependencies.tools`, not `requires.tools`, and leave out Write and Edit even though the skill writes a report and applies fixes. The description doesn't carry the "review", "score" or "health check" phrasings. Several evals hardcode `~/.claude/` and `~/git_repos/claude_ai_playbook/`. |
| **Overall** | **6.1/10** | 2026-10-27 | A sound four-phase audit, held back by evals nothing runs and that don't match the implementation, error cases the reference doesn't document, and a wrong grade in its own worked example. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_review_config/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_review_config/tests/evals.yaml` — Test Coverage dimension
