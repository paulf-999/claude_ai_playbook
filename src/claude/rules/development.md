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
