# 🔨 Rules — Development

These principles apply across all languages and tools used by the team (Python, SQL, Terraform, dbt, Airflow, Bash, Docker, CI/CD). They are cross-cutting concerns that sit above any single style guide — follow them regardless of the technology in use.

---

## 🚨 Error handling

- Always handle errors explicitly — do not let failures pass silently.
- Use `set -e` in all Bash scripts so unexpected errors cause immediate exit.
- Catch specific exceptions in Python — never bare `except:` or `except Exception:`.
- Never run `terraform apply` without first reviewing the plan output — always run `terraform plan` and confirm the diff is expected before applying.
- Log a meaningful message at the point of failure using the appropriate log level.
- Fail fast and surface the problem — do not swallow errors to keep execution going.

---

## ⚙️ Config-driven design

- Externalise environment-specific values (URLs, thresholds, paths, credentials) as parameters or environment variables — never hardcode them in the script or module.
- Scripts and functions should accept inputs (arguments, env vars, config files) rather than embedding assumptions about the environment.
- Keep code portable across dev, UAT, and prod without modification — externalising config makes it testable in isolation.
- Prefer `.env` files for local environment configuration — load them at runtime to supply environment variables. Never commit `.env` files; ensure they are listed in `.gitignore` — see `security.md`.
- Use Jinja templating to parameterise reusable templates (SQL, dbt models, Airflow DAGs, config files) rather than duplicating logic across environments or runs. Keep templates free of hardcoded values — all variable content should be injected at render time.

---

## 🔄 Idempotency

- Scripts, tasks, and pipelines must be safe to re-run — the same inputs must produce the same state with no duplicates or side-effect accumulation.
- SQL: use `MERGE` or `DELETE` + `INSERT` patterns over bare `INSERT`. Never assume a table is empty.
- dbt: models should be fully replaceable on each run; avoid stateful patterns.
- Airflow: tasks must be independently re-runnable. Set `catchup=False` unless backfilling is explicitly required.
- Terraform: resources are declarative — do not work around idempotency with `null_resource` hacks or provisioners where avoidable.
- CI/CD: pipeline runs must be repeatable — do not rely on state left over from a previous run.

---

## 📊 Logging and observability

- Log meaningful operational events — not just errors. At minimum, log the start and end of each significant step.
- Include enough context in log messages to diagnose a failure without needing to re-run: input values, record counts, identifiers.
- Bash: use the log level constants from `shell_utils.sh` — `${DEBUG}` for flow, `${INFO}` for outcomes, `${WARNING}` for recoverable issues, `${ERROR}`/`${CRITICAL}` for failures. See `style_guide_standards/bash.md`.
- Python: use structured log levels consistently — `DEBUG` for flow, `INFO` for outcomes, `WARNING` for recoverable issues, `ERROR`/`CRITICAL` for failures.
- SQL / dbt: surface row counts and merge outcomes in logs or run results. Use Snowflake query tags to attribute queries to the owning pipeline or model.
- Do not log sensitive data (credentials, PII, tokens) — see `security.md`.
- Set threshold-based alerts on job duration, record count, and data freshness — silent failures (a table that stopped updating) are harder to catch than exceptions.
- Track row counts at each pipeline stage; unexpected drops or spikes are early signals of upstream problems.
- Define freshness SLAs per dataset and monitor them; a table that hasn't loaded in 25 hours when it runs daily is a failure even if no exception was raised.

---

## ⚡ Incremental processing

- Process only new or changed records — never reload full datasets when a delta pattern is available.
- SQL / dbt: prefer `incremental` over `table` materialisation for large or frequently-loaded tables; set `unique_key` and choose `strategy` (`merge` / `delete+insert` / `append`) to match data characteristics.
- Airflow: parameterise DAGs on execution date to process bounded time windows; use watermark patterns, not full scans.
- Late-arriving data: define and document a lookback window; do not assume data arrives in strict order.

---

## 🗂️ Data partitioning

- Partition large tables on natural time or business keys so queries scan only what is needed.
- Snowflake: define clustering keys on high-cardinality filter columns (`DATE_TRUNC('day', ...)`, merchant/entity IDs); review clustering health periodically via `SYSTEM$CLUSTERING_INFORMATION`.
- dbt: set partition filter conditions in incremental models to prune micro-partitions on every run — aligning filter columns with cluster keys eliminates full-table scans.
- Avoid cross-partition joins; structure transformations so filters push down naturally.

---

## 🔗 Data lineage

- Every transformation must be traceable from source to final output — if you cannot trace it, you cannot debug or audit it.
- SQL / dbt: always use `ref()` and `source()` — never hardcode schema or table names; this is how lineage is automatically captured and surfaced in the dbt DAG.
- Airflow: declare explicit task dependencies so the DAG graph accurately represents the data flow; do not create implicit dependencies via shared state.
- For transformations that are not self-evident from the code, document upstream dependencies and the business logic applied — a comment at the model or DAG level is sufficient.

---

## 💸 Pipeline cost optimisation

- Analyse expensive queries using Snowflake's Query Profile; attribute pipeline queries via Snowflake query tags (see Logging and observability above).
- Prefer incremental loads over full refreshes — compute cost scales with table size; a full reload that was acceptable at 10M rows is not at 1B rows.
- Right-size Snowflake warehouses: use the smallest warehouse that meets the SLA; configure auto-suspend on all warehouses.
- Choose materialisations deliberately: views incur no write cost but pay at query time; tables invert this — match the choice to query frequency and table size.

---

## 🧹 DRY (Don't Repeat Yourself)

- Every piece of logic, configuration, or data definition should have a single authoritative source. Duplication creates drift — when the same thing exists in two places, they inevitably diverge.
- Python: extract repeated logic into utility functions or shared modules rather than copying code between scripts.
- SQL / dbt: use macros and `ref()` for shared logic — do not copy-paste model logic or column expressions across files.
- Terraform: use modules for repeated resource patterns — do not duplicate provider blocks, variable definitions, or resource configurations.
- Airflow: use shared operators, hooks, and utility functions rather than duplicating DAG logic across pipelines.
- Config: define each environment-specific value once (e.g. in a YAML config or `.env`) and reference it — do not repeat the same value in multiple places.
- CI/CD: extract repeated job steps into reusable workflows or composite actions rather than duplicating pipeline YAML.

---

## 🧩 Modularity

- One function, model, or task should do one thing. Do not bundle unrelated logic.
- Python: keep functions small and single-purpose; compose them rather than growing monolithic scripts.
- dbt: one model per grain. Do not mix aggregation levels or business domains in a single model.
- Airflow: tasks should be atomic — one logical operation per task, not a pipeline-in-a-task.
- CI/CD: one job per concern (lint, test, build, deploy). Do not chain unrelated steps into a single job.

---

## 🧹 Resource cleanup

- Always release resources after use: close database connections, file handles, and HTTP sessions.
- Clean up temporary tables, staging objects, and working files at the end of a script or pipeline run.
- Use context managers (`with` in Python) to guarantee cleanup even when errors occur.
- Do not leave partial state behind that could corrupt a subsequent run.

---

## 🏗️ Immutable infrastructure

- Do not patch running infrastructure — replace it. Changes go through code, not manual edits to live resources.
- Never make manual changes to Terraform-managed resources. All changes must go through `terraform apply`.
- Docker images must use explicit, pinned version tags — never `:latest` in any non-local environment.
- CI/CD: pin action and runner versions explicitly — do not use floating tags such as `@main` or `@v3`.

---

## 📌 Dependency pinning

- Pin all direct dependency versions explicitly:
  - Python: `==` in `requirements.txt`
  - Terraform: `required_providers` block with `version` constraints
  - dbt: `packages.yml` with pinned package versions
  - Docker: base image tags pinned to a specific version
  - CI/CD: GitHub Actions pinned to a specific SHA or immutable tag
- Do not rely on implicit or floating version resolution in any environment beyond local development.
