# 📊 Quality Scorecards

**Purpose:** One home for the quality scorecards that review this config's artefacts — kept apart from rules and skills, since they're review records Claude never reads while working.

---

## 📁 Where each scorecard lives

| Folder | Scores | File pattern |
|---|---|---|
| `agents/` | Agents in `agents/`, one flat folder | `agents/scorecard_<agent_name>.md` |
| `hooks/` | Hooks in `hooks/`, one flat folder | `hooks/scorecard_<hook_name>.md` |
| `rules/` | Rules in `rules/` and `_rules_lazy_load/`, mirroring the rule's current tier, with `rules_lazy_load/` for on-demand rules and `style_guide_standards/` for style guides | `rules/<tier>/scorecard_<rule_name>.md` |
| `skills/` | Skills in `skills/`, one flat folder | `skills/scorecard_<skill_name>.md` |
| `tests/` | Tests in `_tests/`, mirroring the `_tests/` path | `tests/<subpath>/scorecard_<test_file_stem>.md` |

- **Summaries:** each folder has a `<type>_scorecards_summary.md` rollup (e.g. `skills/skill_scorecards_summary.md`) — update it in the same commit as any scorecard change.
  - **Top-level rollup:** `quality_scorecards_summary.md` compares all five types and ranks the next actions.
  - **Template:** all six summaries follow `_templates/scorecard/scorecard_summary.md.template`.
- **Templates:** rules use the template in `rules/README.md`, and skills use `_templates/skills/_quality_scorecard_template.md`.
- **Never `@import`:** these files are for review and audit only, so they cost no session tokens.
- **Audits:** cross-cutting audits of whole areas live in the playbook repo under `docs/audits/`, not here.

---

## 🔍 Independent review

Skills, rules and agents are scored by a reviewer that didn't write them, so the author never marks their own work.

1. **Deterministic checks:** `make lint` and `CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest` pass before any scoring.
2. **Evals:** the artefact's evals exist at the count its maturity needs.
   - **Agents:** run `python3 src/claude/scripts/_audit_scripts/audit_agent_evals.py <agent>` and give the reviewer its pass rate, which costs one Claude call per runnable eval.
3. **Fresh-context review:** call the Agent tool with `subagent_type: quality_scorecard_reviewer`, passing only the artefact's path and its type.
   - **Its inputs:** the artefact, its contract, its evals, the type's rubric and `scoring_anchors.md`.
   - **Never pass:** the authoring conversation or the current scorecard's scores, since either would anchor the result.
4. **History row:** append the row it returns to `score_history.csv` as the next attempt, then copy the scores into the scorecard and its summaries.
   - **Enforced by:** `test_score_history.py`, which fails when attempts skip or the latest row doesn't match the scorecard.
5. **Human review:** a CODEOWNERS reviewer approves the scorecard change in the PR.

- **Anchors:** `scoring_anchors.md` shows what a 5, a 7 and a 9 look like for each type.
- **Seed rows:** attempt 1 for every scorecard that existed before this flow says `reviewer=author`, since those scores were self-assessed.
- **Not yet covered:** hooks and tests keep author scoring for now.

---

## 🚀 Top 5 recommended actions

The five lowest-scoring artefacts, each with the first recommended improvement from its scorecard.

| # | Artefact | Score | Action | Scorecard |
|---|---|---|---|---|
| 1 | `claude_review_config` | 6.1 | Fix the grade in SKILL.md's Example Usage: 7.7/10 should be B, not B+ | [scorecard_claude_review_config.md](skills/scorecard_claude_review_config.md) |
| 2 | `dbt.md` | 6.2 | Make the source-test requirement say the same thing in every section, and define "completeness" or drop it | [scorecard_dbt.md](rules/style_guide_standards/scorecard_dbt.md) |
| 3 | `makefile.md` | 6.2 | Bring the repo's own Makefiles into line with the guide, or record the exceptions | [scorecard_makefile.md](rules/style_guide_standards/utilities/scorecard_makefile.md) |
| 4 | `terraform.md` | 6.2 | Read the Snowflake private key path from a variable, or state it as the one allowed exception to "never hardcoded" | [scorecard_terraform.md](rules/style_guide_standards/infra/scorecard_terraform.md) |
| 5 | `technical_writer` | 6.3 | Decide whether the agent drafts Confluence pages, then make its description, triggers and evals agree | [scorecard_technical_writer.md](agents/scorecard_technical_writer.md) |

- **Ties:** three style guides score 6.2 and rank alphabetically, and `technical_writer` ranks above `airflow.md`, also 6.3, because an agent acts while a style guide only advises.
- **Upkeep:** refresh this list whenever a scorecard is re-scored.
- **Full ranking:** see `quality_scorecards_summary.md`.
