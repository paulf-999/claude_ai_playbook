# Quality Scorecard — confluence_create_page

**Date Created:** 2026-09-19
**Date Updated:** 2026-10-27

**Overall score:** 5.7/10

**Recommended improvements:**
- Rewrite evals 4–7, 9 and 10 against the prose skill, or delete them, since they test Python functions (`validate_title`, `phase_2_validate`, `create_page_with_timeout` and others) that exist nowhere under `src/`
- Add evals for each `not_for` case (bulk creation, page updates, an unsupported pattern) and for pasted content that contains instructions
- Rewrite `reference/_troubleshooting.md` to match the current skill, removing flags that don't exist, the git-config creator lookup, keyword-based titles and `~/.claude/logs/`
- Describe how the publish timeout is handled at run time in `_phases.md`, or remove "Timeout protection" from SKILL.md's Purpose
- Delete or merge `reference/_confluence_page_formatting.md`, which repeats `common/_common_header.md` and `common/_common_formatting.md` and has drifted
- Add `reference/_implementation.md`, or rename `_phases.md` to it, to meet hard gate 6
- Make the created and updated dates agree across the header, frontmatter and contract
- Remove `mcp__atlassian__updateConfluencePage` from `tools`, and drop the `not_for` pointer to `/confluence_update_page`, which doesn't exist
- Say how the title, space key and section names are checked before they reach Confluence

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | • 📐 **Sound:** pick pattern, follow pattern, then a mandatory Local Draft Review, with detail in `reference/`<br>• ⚠️ **Two jobs:** the publish step sits inside each pattern file behind "do not execute this yet"<br>• 🌫️ **No design:** SKILL.md's "Timeout protection" has nothing behind it at run time |
| **Complexity** | 5/10 | 2026-10-27 | • 🧮 **Raw complexity 5:** Concepts 2, Scope 1, Dependencies 1 (Atlassian MCP), Prerequisites 1 (MCP enabled, space access)<br>• ✅ **Within the cap:** inside the tactical limit of 6 |
| **Test Coverage** | 4/10 | 2026-10-27 | • 👻 **Phantom targets:** 6 of 10 evals assert on Python functions that exist nowhere, so only 4 test the real skill<br>• 🕳️ **Gaps:** no eval for a `not_for` case or untrusted input, and nothing runs them<br>• ⚠️ **Overstated:** `test_coverage_level: comprehensive` and `tested: true` |
| **Code Quality** | 6/10 | 2026-10-27 | • ✅ **Safe patterns:** draft before publish, `status: draft`, a confirmed parent and never the space root<br>• 🕳️ **Missing:** no runtime file defines input validation<br>• ⚠️ **Thin recovery:** `_error_recovery.md` says little, and the phases never say to keep the draft when publishing fails |
| **Security** | 7/10 | 2026-10-27 | • 🔒 **Confirmed:** explicit draft approval even when asked to "just publish", created as a draft, space and parent confirmed, no personal names<br>• ⚠️ **Gaps:** user-supplied page content isn't treated as data, and no eval covers injection<br>• ⚠️ **Broad tools:** `updateConfluencePage` is granted but not needed |
| **Documentation** | 5/10 | 2026-10-27 | • ✅ **Clear:** SKILL.md has a realistic example and caveats<br>• 🍂 **Stale:** `_troubleshooting.md` mostly describes a different implementation, sending users after things that aren't there<br>• ⚠️ **Duplicate:** a second formatting file, and no FAQ |
| **Standards Compliance** | 6/10 | 2026-10-27 | • ✅ **Met:** naming, contract fields, SKILL.md structure and length, emoji headings, `tests/` layout and version 1.4.1<br>• ❌ **Missed:** no `reference/_implementation.md` (gate 6) and no runtime input validation (gate 9)<br>• ⚠️ **Drift:** dates disagree across files, and the evals' phase labels don't match `_phases.md` |
| **Overall** | **5.7/10** | 2026-10-27 | Safe, well-structured draft-then-publish flow, but most of its tests and troubleshooting docs describe a Python version of the skill that no longer exists. |

## 🔗 Related files

- `src/claude/skills/_atlassian_skills/confluence_create_page/SKILL.md` — the skill being scored
- `src/claude/skills/_atlassian_skills/confluence_create_page/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored by `quality_scorecard_reviewer`, which saw the attempt 1 Overall while finding the attempt number
