# Quality Scorecard — confluence_create_page

**Date Created:** 2026-09-19
**Date Updated:** 2026-10-29

**Overall score:** 6.9/10

**Recommended improvements:**
- Add a runner or pytest that executes `tests/evals.yaml`, or set `tested: false` and lower `test_coverage_level` until one exists
- Delete `reference/_confluence_page_formatting.md` or make it the one source, since it repeats `reference/common/_common_header.md` and `_common_formatting.md`, and SKILL.md links to one copy while the patterns read the other
- Change `_error_recovery.md`'s "Try again: transient errors are common" so it says what `_troubleshooting.md` says: check the parent page for a new draft before retrying, so a retry doesn't create a duplicate
- Remove `mcp__atlassian__updateConfluencePage` from the SKILL.md `tools:` list, since the contract marks page updates as `not_for`
- Add an instruction to treat pasted or imported page content as data, not instructions, and add an eval for it
- Make the three creation dates agree (frontmatter `2026-06-07`, metadata header `2026-04-08`, contract `2026-08-28`)
- Change the Example Usage so it shows a draft being created (it says "Publishing… Page created"), and add an eval for a "just publish" request with no approval

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | Clear phases (pre-check, page type, pattern, draft review, publish), with the detail kept in `reference/`. One phase does two jobs: each pattern file both gathers content and holds the deferred "Create the Confluence page" step, so publishing is split across three files. The formatting rules exist twice (`_confluence_page_formatting.md` and `common/`), which will drift. |
| **Complexity** | 5/10 | 2026-10-27 | Raw 5: Concepts 2 (two patterns, draft review, ADF publish, constraints), Scope 1 (skill folder with `patterns/` and `common/`, plus a write to `~/_drafts/`), Dependencies 1 (Atlassian MCP), Prerequisites 1 (MCP enabled and write access to the space). Matches the ~5 anchor: several jobs, several folders, one external service. Within the tactical limit of 6. |
| **Test Coverage** | 7/10 | 2026-10-29 | 10 evals, inside the tactical range of 8–12. They cover both happy paths, MCP unavailable, space and parent confirmation, name replacement, draft iteration, permission denied, and two `not_for` cases (unsupported pattern, page update). They are prose that nothing runs: no `_tests/skills/confluence_create_page/` exists. The unrun-evals cap of 7 applies, and `tested: true` / `test_coverage_level: comprehensive` overstate this. There is no eval for a publish timeout or a duplicate on retry, or for "just publish" with no approval. |
| **Code Quality** | 7/10 | 2026-10-29 | No code. The prompt logic checks inputs (slug rules, space and parent confirmed, `~` expanded before Write) and stops early when the MCP pre-check fails. Error handling is thin and contradicts itself: `_error_recovery.md` says "Try again: transient errors are common", while `_troubleshooting.md` says to check for a new draft first to avoid a duplicate. |
| **Security** | 7/10 | 2026-10-27 | Has a confirm step: no create call before draft approval, `status: draft`, and `confirmation_required: true` in the contract. Permissions are scoped to create and view. Matches the ~7 anchor because nothing says to treat user-supplied or pasted content as data, not instructions. The `tools:` list also grants `updateConfluencePage`, one tool more than the job needs. |
| **Documentation** | 8/10 | 2026-10-29 | The purpose, prerequisites and caveats (only two patterns, the wide view is set by hand) are clear. `_troubleshooting.md` covers real symptoms (stray `~` folder, failure part-way through a publish, draft-only page). There is no FAQ. The Example Usage shows "Publishing… ✓ Page created", which hides that the page is created as a draft, and its `(y/e/n)` prompt appears nowhere in `_implementation.md`. |
| **Standards Compliance** | 7/10 | 2026-10-29 | Passes: naming, a complete contract with specific `not_for`, version 1.5.0 matching, emoji headings, about 56 lines excluding the Instructions section, evals in `tests/` with a README, and `_implementation.md` present. Misses: `tested: true` with no behavioural test, three different creation dates, and the draft path given as `~/_drafts/...` with an "expand `~`" note instead of a `$HOME`-based path. |
| **Overall** | **6.9/10** | 2026-10-29 | A sound tactical skill with a real approval gate, held back by evals nothing runs, duplicated formatting references and error guidance that contradicts itself. |

## 🔗 Related files

- `src/claude/skills/_atlassian_skills/confluence_create_page/SKILL.md` — the skill being scored
- `src/claude/skills/_atlassian_skills/confluence_create_page/tests/evals.yaml` — Test Coverage dimension
