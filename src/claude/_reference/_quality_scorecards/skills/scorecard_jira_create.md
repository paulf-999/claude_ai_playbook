# Quality Scorecard — jira_create

**Date Created:** 2026-09-19
**Date Updated:** 2026-10-27

**Overall score:** 5.7/10

**Recommended improvements:**
- Set `output.confirmation_required: true` in `skill.contract.yaml` and remove the "execute immediately without permission gates" comments, so the contract matches SKILL.md's "wait for a yes" rule
- Rewrite `tests/evals.yaml` to assert on Claude's behaviour, not on functions that don't exist (`phase_2_validate`, `validate_story_points`, `create_jira_ticket`, `MIN_STORY_POINTS`)
- Add evals for a `not_for` request (for example "update PROJ-12"), the confirm-before-create step, a request with no project named, and pasted description text
- Add `reference/_implementation.md` with the phases and the confirm step, and show the confirm and project steps in Example Usage
- Fix the contradictions in `_field_constraints.md` and `_error_handling.md`: the story point upper limit, an empty description, Epic as a valid type, and "assumes a default Jira project"
- Add `getAccessibleAtlassianResources` to `tools:` and `requires.tools`, and change the `~/.claude/` paths to `$HOME`-based ones
- Put the phrases users type into the frontmatter `description`, and remove `test_coverage_level: comprehensive` or back it with security evals

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 6/10 | 2026-10-27 | • ✅ **Focused:** one clear purpose and a sensible Task default<br>• ⚠️ **Contradiction:** SKILL.md says to wait for a yes before creating, while the contract says "execute immediately; no preliminary confirmations"<br>• 🕳️ **Missing:** Example Usage merges validation and creation with no confirm or project step, and no `_implementation.md` records the phases |
| **Complexity** | 6/10 | 2026-10-27 | • 🧮 **Raw complexity 4:** Concepts 1, Scope 1 (read-only pointers to `jira.md` and `org.md`), Dependencies 1 (Atlassian MCP), Prerequisites 1 (MCP enabled and restarted)<br>• ⚠️ **At the cap:** right at the draft limit of 4 |
| **Test Coverage** | 5/10 | 2026-10-27 | • 📊 **Draft count:** 6 evals, inside 5–8<br>• 👻 **Phantom targets:** the assertions target code that doesn't exist, though `tests/README.md` says the skill has no Python code<br>• 🕳️ **Gaps:** no eval for a `not_for` case, the confirm step, project confirmation or adversarial input, and nothing runs them |
| **Code Quality** | 6/10 | 2026-10-27 | • ✅ **Errors covered:** MCP, 403, 404 and assignee failures<br>• ⚠️ **Contradictions:** story points "0.5 to 100" then "no upper limit", description "Required" yet "can be empty", and Epic valid though epics are `not_for`<br>• ⚠️ **Missing tool:** the pre-check calls `getAccessibleAtlassianResources`, which isn't in `tools:` |
| **Security** | 6/10 | 2026-10-27 | • 🔒 **In SKILL.md:** a confirm step and "never infer the Jira project"<br>• ⚠️ **Undercut:** the contract sets `confirmation_required: false` on an irreversible external write<br>• ⚠️ **Gaps:** pasted ticket text isn't treated as data, and `_field_constraints.md` assumes a default project |
| **Documentation** | 6/10 | 2026-10-27 | • ✅ **Clear:** purpose, Best For caveats and the error-recovery guide<br>• ⚠️ **Contradiction:** the example has no confirm step, against the Always rule<br>• ⚠️ **Unbacked:** "gaps logged as TODOs" with no TODO recorded, and unverified recovery steps<br>• ❓ **No FAQ** |
| **Standards Compliance** | 5/10 | 2026-10-27 | • ✅ **Met:** naming, a 0.2.4 header matching the contract, `tests/README.md` and eval count<br>• ❌ **Missed:** no `_implementation.md` (gate 6), an irreversible write without confirmation (gate 2), no trigger phrases and `~/.claude/` paths (gate 3)<br>• ⚠️ **Misplaced:** the write permission sits in `requires.external`, not `dependencies.permissions` |
| **Overall** | **5.7/10** | 2026-10-27 | The flow is short and usable, but it can't be trusted yet: the contract waives the confirm step SKILL.md requires, and the evals test code that doesn't exist. |

## 🔗 Related files

- `src/claude/skills/_atlassian_skills/jira_create/SKILL.md` — the skill being scored
- `src/claude/skills/_atlassian_skills/jira_create/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored by `quality_scorecard_reviewer`, which saw an earlier score in `README.md` and `scoring_anchors.md`
