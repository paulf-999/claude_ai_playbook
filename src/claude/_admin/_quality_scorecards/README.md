# 📊 Quality Scorecards

**Purpose:** One home for the quality scorecards that review this config's artefacts — kept apart from rules and skills, since they're review records Claude never reads while working.

---

## 📁 Where each scorecard lives

| Folder | Scores | File pattern |
|---|---|---|
| `rules/` | Rules in `_rules/`, mirroring the tier path | `rules/<tier>/scorecard_<rule_name>.md` |
| `skills/` | Skills in `skills/`, one flat folder | `skills/scorecard_<skill_name>.md` |
| `hooks/` | Hooks in `hooks/` — none scored yet | `hooks/scorecard_<hook_name>.md` |
| `agents/` | Agents in `agents/` — none scored yet | `agents/scorecard_<agent_name>.md` |
| `tests/` | Tests in `_tests/`, mirroring the `_tests/` path | `tests/<subpath>/scorecard_<test_file_stem>.md` |

- **Summaries:** each folder has a `<type>_scorecards_summary.md` rollup (e.g. `skills/skill_scorecards_summary.md`) — update it in the same commit as any scorecard change.
  - **Top-level rollup:** `quality_scorecards_summary.md` compares all five types and ranks the next actions.
- **Templates:** rules use the template in `rules/README.md`, and skills use `_templates/skills/_quality_scorecard_template.md`.
- **Never `@import`:** these files are for review and audit only, so they cost no session tokens.
- **Audits:** cross-cutting audits of whole areas live in `_admin/_audits/`, not here.
