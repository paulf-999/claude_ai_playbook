# Quality Scorecard — jira_create

**Date Created:** 2026-09-19
**Date Updated:** 2026-10-29

**Overall score:** 6.4/10

**Recommended improvements:**
- Drop Epic from the valid issue types in `_field_constraints.md` and `_error_handling.md`, because `not_for` and Best For both say the skill can't create epics
- Settle the story-points limit: `_field_constraints.md` gives "Valid range: 0.5 to 100" and also "no upper limit enforced"
- Set `tested: false` until a runner or a pytest runs `tests/evals.yaml`, because nothing under `_tests/skills/` covers `jira_create`
- Change `test_coverage_level: comprehensive` to `basic` or add the missing security case, and remove the contract note "error handling incomplete" that `_error_handling.md` no longer supports
- Fix the `waives_response_standards` comment ("3-phase … gather → create → confirm") so it matches the six phases, where confirm comes before create
- Add a `dependencies.permissions` entry for Jira write access, and remove "security checks" from the contract `summary`, since there aren't any
- Add evals for Jira 403 and assignee-not-found errors, for pasted ticket text that contains instructions, and for at least one more `not_for` case, such as an epic
- Have the skill treat pasted or quoted content as data rather than instructions when drafting the description
- Replace the literal `~/.claude/` paths in References with paths that resolve to the config directory, as `portable_paths.md` requires

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-29 | The phase table in `_implementation.md` is clean, with one job per phase and the detail kept in `reference/`. The scope contradicts itself, though: `_field_constraints.md` lists "Valid values: Bug, Task, Improvement, Epic", while `not_for` says "creating epics (v2.0+)". |
| **Complexity** | 6/10 | 2026-10-27 | The raw sum is 4: Concepts 1 (project, story-point and confirm rules), Scope 1 (its own `reference/` plus the `jira.md` read), Dependencies 1 (Atlassian MCP) and Prerequisites 1 (MCP enabled). That sits right at the Draft limit of 4. |
| **Test Coverage** | 7/10 | 2026-10-29 | There are 8 evals, the right count for Draft, and one `not_for` case (`update_request_out_of_scope`). The cap applies because they are prose that nothing runs. No eval covers a Jira 403 or assignee error, injected text, or the other five `not_for` entries. |
| **Code Quality** | 6/10 | 2026-10-27 | Validation and error paths are written down, but the field rules contradict each other. Story points are "0.5 to 100" and also "no upper limit enforced". Description is "Required: Yes" and also "Can be empty string". |
| **Security** | 7/10 | 2026-10-29 | The skill shows the full ticket and waits for a yes, and `confirmation_required: true` now matches SKILL.md. It uses only three tools. Nothing says pasted or quoted content in "log this as a Jira ticket" is data, not instructions. |
| **Documentation** | 6/10 | 2026-10-27 | Purpose, Example Usage and Best For are clear. The contract `summary` promises "security checks" that don't exist. Best For says "gaps logged as TODOs", but no file records them. References use literal `~/.claude/` paths, which don't resolve on a `~/claude/` install. |
| **Standards Compliance** | 6/10 | 2026-10-29 | Naming, structure, the length limit, the metadata header and matching versions (0.4.0) all pass. There is no `dependencies.permissions` block (hard gate 2). The frontmatter claims `tested: true` with no behavioural test in `_tests/skills/`. The contract says `test_coverage_level: comprehensive` alongside "Draft maturity: happy path only; error handling incomplete". |
| **Overall** | **6.4/10** | 2026-10-29 | A sound, well-confirmed Draft skill held back by contradictions between its contract, field rules and scope, plus evals that nothing runs. |

## 🔗 Related files

- `src/claude/skills/_atlassian_skills/jira_create/SKILL.md` — the skill being scored
- `src/claude/skills/_atlassian_skills/jira_create/tests/evals.yaml` — Test Coverage dimension
