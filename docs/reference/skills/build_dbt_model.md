# /build_dbt_model — dbt model delivery

End-to-end dbt model delivery: reads Jira requirements, designs the model, produces a
source-to-target mapping, writes the SQL, tests in UAT, defines dbt tests, writes a test plan,
and updates the Jira ticket.

Invoke with `/build_dbt_model` in Claude Code from the `da-etl-dbtanalytics` repo.

---

## Prerequisites

- Atlassian MCP server active (`make enable_mcp server=Atlassian`, then restart Claude Code)
- Snowflake read access via `prd_sel_role`
- dbt configured with a UAT target
- `PRIVATE_KEY_PASSPHRASE` available in `/home/karl/git_repos/.env`

---

## How to start

Invoke `/build_dbt_model` and provide the Jira ticket key when prompted. Claude fetches the
ticket, extracts requirements, and asks any remaining clarifying questions in a single message.

---

## Phases

**Phase 1 — Gather requirements from Jira**
Fetches the ticket via Atlassian MCP. Extracts source tables, target model name, layer,
grain, business logic, and acceptance criteria. Asks all clarifying questions at once.

**Phase 2 — Design and S2T mapping**
Reasons through layer placement, CTE structure, join strategy, surrogate key inputs, and
aggregations. Produces a source-to-target mapping table saved to `docs/s2t/<model_name>_s2t.md`.
Requires explicit approval before writing any SQL.

**Phase 3 — Build / update the dbt model**
Writes the SQL to the correct layer path. Follows team standards: leading commas, 4-space
indent, explicit JOIN types, CTEs only, `create_surrogate_key`, `limit_rows()`. Creates or
updates the YAML properties file with column descriptions and KEY tests.

**Phase 4 — Test in UAT**
Displays the exact `dbt run` command and waits for approval. After a successful run, queries
UAT for row count and sample rows. Halts if row count is 0 (unexpected) or the run fails.

**Phase 5 — Test plan**
Adds dbt YAML tests (unique + not_null on KEY, relationship tests on FKs, not_null on
non-nullable columns). Writes a markdown test plan to `docs/test_plans/<model_name>_test_plan.md`.

**Phase 6 — Write back to Jira**
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

| Artefact | Path |
|---|---|
| dbt SQL model | Layer-dependent (see above) |
| YAML properties | Co-located `.yml` file |
| S2T mapping | `docs/s2t/<model_name>_s2t.md` |
| Test plan | `docs/test_plans/<model_name>_test_plan.md` |

---

## Approval gates

The skill pauses for explicit confirmation at three points:

1. **Before writing SQL** — after Phase 2 design review
2. **Before `dbt run`** — displays exact command
3. **Before posting the Jira comment** — displays full comment text

---

## SQL standards applied

- Leading commas, 4-space indent, UPPERCASE keywords
- Explicit JOIN types (`INNER JOIN`, `LEFT JOIN`)
- CTEs only — no subqueries
- `{{ create_surrogate_key([...]) }} AS "KEY"` as the first column
- `{{ limit_rows() }}` on the final SELECT and major intermediate CTEs
- Audit fields via `{{ dbt_last_modified_field() }}` where applicable

---

## Key paths

| Item | Value |
|---|---|
| dbt project root | `/home/karl/git_repos/da-etl-dbtanalytics/prod_analytics/` |
| Snowflake access | `snow sql -c prd_sel_role` |
| Env file | `/home/karl/git_repos/.env` |
| S2T docs | `docs/s2t/` |
| Test plan docs | `docs/test_plans/` |
