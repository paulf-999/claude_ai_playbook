# 🧪 Rules — Testing

## ✅ General

- Do not consider a task complete unless tests exist and pass.
- If no tests cover the area being changed, flag the gap before proceeding and agree on what to add.
- Do not work around missing tests — surface the gap first.
- Do not use `--no-verify` to bypass pre-commit hooks unless explicitly instructed.

---

## 🐍 Python

- Use `pytest` for all unit and integration tests.
- Tests live in a `tests/` directory mirroring the source structure.
- All new functions must have corresponding unit tests.
- Run tests locally before raising a PR.

---

## 🔄 dbt

- Every dbt model must have at least `not_null` and `unique` tests on primary key columns.
- Use singular tests for business logic that cannot be expressed as generic tests.
- `dbt test` must pass before a PR is raised.
- Source freshness checks should be defined where data latency matters.

---

## 🗄️ SQL / data quality

- Validate assumptions about grain, nulls, and deduplication before finalising a query.
- Flag unexpected row counts, distributions, or nulls encountered during development.
- Do not assume referential integrity unless it is enforced or tested.

---

## 🪝 Pre-commit

- Pre-commit hooks must pass on every commit.
- If a hook fails, fix the underlying issue — do not suppress or bypass.
