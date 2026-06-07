# /dq-check — DQ Framework test creation

Creates a new SOURCE_ONLY DQ Framework test end-to-end: inspects the Snowflake tables,
writes the dbt model, appends the row to `test_metadata.csv`, and verifies the check runs.

Invoke with `/dq-check` in Claude Code from either the `dmt-dq_framework-v2` or
`da-etl-dbtanalytics` repo.

---

## Prerequisites

- Snowflake read access via `prd_sel_role`
- Access to dbt with a prod target for `dbt run` and `dbt seed`

---

## How to start

Paste the **Jira ticket description** (or any plain-English description of the check) when
prompted. Claude extracts what it can from the description, then asks only the clarifying
questions needed to fill in the gaps — all in a single message.

Things Claude will try to infer from the description:

| Item | Example |
|---|---|
| Source table (left side of check) | `DIM_BUSINESS_UNIT` |
| Target/rollup table to check against | `DIM_BUSINESS_UNIT_ROLLUP` |
| Join key column (present in both) | `BUSINESS_UNIT_ID` |
| Filter condition on source (optional) | `IS_ACTIVE = TRUE` |
| Columns to return when check fails | `BUSINESS_UNIT_ID`, `BUSINESS_UNIT_NAME` |
| Short test name (max 100 chars) | `BU missing from BU rollup` |
| One-sentence description | `Active BUs with no entry in DIM_BUSINESS_UNIT_ROLLUP. 0 rows = pass.` |

After the clarifying questions are answered, the skill proceeds automatically.

---

## Steps

**1 — Gather requirements**
Asks for the Jira ticket description. Extracts what it can, then asks clarifying questions
for anything not clear from the description — all in a single message.

**2 — Inspect tables in Snowflake**
Runs `DESCRIBE TABLE` on both tables via `prd_sel_role` to confirm the join key and filter
column exist. Stops and reports back if anything is missing.

**3 — Write the dbt model**
Creates `dq_<name>.sql` in the appropriate `models/dq_framework/` subdirectory.
Pattern: LEFT JOIN, `WHERE tgt.<join_key> IS NULL` (+ optional filter). 0 rows returned = pass.

**4 — Look up TEST_GRP_ID and next TEST_ID**
Queries `GROUP_REFERENCE`, `CONNECTION`, and `MAX(TEST_ID)` from `TEST_METADATA` via
the framework's Python connection. Confirms group and connection with you if not obvious from
context. Common defaults for warehouse/DIM checks: group **64** (`DIM TABLE QUALITY CHECKS`),
connection **7** (`SNOWFLAKE-ETL-KEY-PAIR`).

**5 — Build the SOURCE_SQL**
```sql
SELECT * FROM DQ_FRAMEWORK.<SCHEMA>.<MODEL_NAME>;
```

**6 — Append to test_metadata.csv**
Appends the new row to:
```
prod_analytics/data/dq_framework/test_metadata.csv
```
Does **not** insert directly into Snowflake — the CSV is the source of truth.

**7 — dbt compile (optional)**
Confirms the model parses and `ref()` targets resolve. Skipped if browser SSO is unavailable.

**8 — Verify SOURCE_SQL**
Runs the SOURCE_SQL directly via `prd_sel_role` and reports the violation row count and
sample rows.

---

## After the skill: materialise and sync

The skill does not run `dbt run` or `dbt seed` — those require explicit approval and are
run separately after the PR is raised.

**Materialise the view** (creates it in Snowflake):
```
dbt run -s <model_name> -t prod
```

**Sync the seed** (writes `test_metadata.csv` rows into `TEST_METADATA` in Snowflake):
```
dbt seed -s test_metadata -t prod
```

Claude will ask for your approval before running either command.

---

## DQ check schemas

The target schema depends on what is being checked — `WAREHOUSE_CHECKS` is one of several:

| Schema | Check type |
|---|---|
| `WAREHOUSE_CHECKS` | DIM/warehouse referential integrity |
| `BASE_DATA_CHECKS` | Base layer data quality |
| `RESIDUALS_CHECKS` | Residuals data integrity |
| `TRANSACTION_CHECKS` | Transaction data |
| `PLATFORM_CHECKS` | Platform and process control |
| `DATA_SRC_CHECKS_ACCESS_ONE` | Access One source data |
| `DATA_SRC_CHECKS_BANQUEST_IRIS` | Banquest/IRIS source data |
| `DATA_SRC_CHECKS_PPS` | PPS source data |
| `DATA_SRC_CHECKS_MISC` | Miscellaneous source checks |
| `DQ_DATA_SRC` | General data source checks |

---

## Test types

| Type | Logic | Pass condition |
|---|---|---|
| `SOURCE_ONLY` | Runs one SQL query | 0 rows returned |
| `SOURCE_VS_TARGET` | Runs two queries and compares DataFrames | Results are identical |
| `AI_ANOMALY` | Runs a detector, returns anomaly score 0.0–1.0 | Score < 0.4 |

The `/dq-check` skill creates `SOURCE_ONLY` checks.

---

## Key paths

| Item | Value |
|---|---|
| dbt model path | `prod_analytics/models/dq_framework/<schema_subfolder>/` |
| Seed CSV | `prod_analytics/data/dq_framework/test_metadata.csv` |
| Skill definition | `~/.claude/plugins/marketplaces/payroc-agent-skills/plugins/test-eng/dq-check/` |
| Streamlit test runner | `http://localhost:8501` (manual testing — does not send alerts) |
