# /warehouse_design — data model delivery

End-to-end data model delivery: reads Jira requirements, designs the model, produces a
source-to-target mapping, publishes a Confluence design page, gets sign-off, writes the SQL,
tests in UAT, defines dbt tests, writes a test plan, and updates the Jira ticket.

Invoke with `/warehouse_design` in Claude Code from the `da-etl-dbtanalytics` repo.

---

## Prerequisites

- Atlassian MCP server active (`make enable_mcp server=Atlassian`, then restart Claude Code)
- Snowflake read access via `prd_sel_role`
- dbt configured with a UAT target
- `PRIVATE_KEY_PASSPHRASE` available in `/home/karl/git_repos/.env`

---

## How to start

Invoke `/warehouse_design` and provide the target model name when prompted. Claude checks for
an in-progress WIP file and either resumes or starts fresh. If starting fresh, it asks for the
Jira ticket key and gathers all clarifying questions in a single message.

---

## Session persistence

A WIP file at `docs/design/<model_name>_wip.md` in the dbt project preserves state across
sessions. If the file exists when the skill starts, Claude summarises progress and asks whether
to resume or start over.

The WIP file is local session tracking only — do not commit it to the repo. The authoritative
design record is the Confluence page published in Phase 3.

---

## Phases

**Phase 1 — Gather requirements from Jira**
Fetches the ticket via Atlassian MCP. Extracts source tables, target model name, layer,
grain, business logic, and acceptance criteria. Asks all clarifying questions at once,
grouped by category (source data, target model, business logic, delivery).

**Phase 2 — Design and S2T mapping**
Reasons through layer placement, CTE structure, join strategy, surrogate key inputs, and
aggregations. Produces a source-to-target mapping table published to Confluence in Phase 3.

**Phase 3 — Confluence design page**
Publishes a design page under the "Data Model - Design" space, organised by business domain.
Creates a domain index page if one does not exist. Reports the Confluence page URL.

*Design approval gate* — presents a summary (layer, materialisation, grain, S2T path, Confluence
URL) and waits for explicit "yes" / "proceed" before starting Phase 4.

**Phase 4 — Build / update the dbt model**
Writes the SQL to the correct layer path. Follows team standards: leading commas, 4-space
indent, explicit JOIN types, CTEs only, `create_surrogate_key`, `limit_rows()`. Creates or
updates the YAML properties file with column descriptions and KEY tests.

**Phase 5 — Test in UAT**
Displays the exact `dbt run` command and waits for approval. After a successful run, queries
UAT for row count and sample rows. Halts if row count is 0 (unexpected) or the run fails.

**Phase 6 — Test plan**
Adds dbt YAML tests (unique + not_null on KEY, relationship tests on FKs, not_null on
non-nullable columns). Writes a markdown test plan to `docs/test_plans/<model_name>_test_plan.md`.

**Phase 7 — Write back to Jira**
Shows a comment preview before posting. Posts via Atlassian MCP on confirmation. Offers to
apply a status transition (shows available transitions, waits for selection).

---

## Model paths

| Layer | Path |
|---|---|
| Warehouse | `prod_analytics/models/warehouse/<model_name>.sql` |
| Intermediate | `prod_analytics/models/intermediate/<domain>/<model_name>.sql` |
| Other | Asked at runtime |

---

## Output artefacts

| Artefact | Path / Location | Committed to repo? |
|---|---|---|
| dbt SQL model | Layer-dependent (see above) | Yes |
| YAML properties | Co-located `.yml` file | Yes |
| Test plan | `docs/test_plans/<model_name>_test_plan.md` | Yes |
| Confluence design page | Under "Data Model - Design" > `<Domain>` | No — lives in Confluence |
| S2T mapping | Sub-page of Confluence design page | No — lives in Confluence |
| Design WIP file | `docs/design/<model_name>_wip.md` | No — local session tracking only |

---

## Approval gates

The skill pauses for explicit confirmation at four points:

1. **Before writing SQL** — after Phase 3 design review and Confluence page published
2. **Before `dbt run`** — displays exact command
3. **Before posting the Jira comment** — displays full comment text
4. **Before status transition** — shows available transitions, waits for selection

---

## SQL standards applied

- Leading commas, 4-space indent, UPPERCASE keywords
- Explicit JOIN types (`INNER JOIN`, `LEFT JOIN`)
- CTEs only — no subqueries
- `{{ create_surrogate_key([...]) }} AS "KEY"` as the first column
- `{{ limit_rows() }}` on the final SELECT and major intermediate CTEs
- Audit fields via `{{ dbt_last_modified_field() }}` where applicable

---

## fact_residual domain

When working in the `fact_residual` domain, note the two source patterns:

| Pattern | Examples | In `combined_sources`? |
|---|---|---|
| Passage file sources | `fact_residual_apps`, `fact_residual_tsys` | Yes (via `attributes`) |
| Bypass sources | `fact_residual_manual_adjustment`, `fact_residual_netsuite_revenue` | No (direct ref in `unioned`) |

New bypass sources go in `1_fact_residual_source/` and are added directly to
`fact_residual_unioned.sql` — not to `fact_residual_combined_sources`.

---

## Key paths

| Item | Value |
|---|---|
| dbt project root | `/home/karl/git_repos/da-etl-dbtanalytics/prod_analytics/` |
| Snowflake access | `snow sql -c prd_sel_role` |
| Env file | `/home/karl/git_repos/.env` |
| Design WIP files | `docs/design/` (local only — not committed) |
| Test plan docs | `docs/test_plans/` |
| Confluence parent | Data Model - Design (page ID `2328297573`, space `DA`) |
