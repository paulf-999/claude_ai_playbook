# 🔗 Data Lineage

## What lineage means in practice

Lineage is the ability to trace any value in a final output back to its source — through every transformation step. Without it, debugging data quality issues requires reverse-engineering the pipeline from scratch.

A pipeline has adequate lineage when:
- Every input dataset is declared explicitly (not inferred or hardcoded)
- Every transformation step is named and ordered
- Upstream dependencies are visible without running the pipeline

---

## Declaring dependencies

**dbt:** use `ref()` for all model-to-model references and `source()` for all raw source references. Never hardcode schema or table names — `ref()` and `source()` are how the dbt DAG is built and how lineage is surfaced in the docs site.

**Airflow:** declare task dependencies explicitly with `>>` / `<<` operators or `set_downstream()`. Do not create implicit dependencies via shared state (e.g. writing to a file in task A and reading it in task B without an explicit dependency edge).

**Bespoke SQL pipelines:** declare input tables in a comment block at the top of the script — list each source table and what it contributes. This is the minimum viable lineage for pipelines outside of dbt.

---

## Documenting non-obvious transformations

Lineage tools show *what* feeds into *what* — they do not explain *why* a transformation exists or *what business logic* it applies. Document at the model or task level when:

- A column is derived from multiple sources in a non-obvious way
- A filter discards records for a business reason (not a technical one)
- A join uses a non-obvious key or has known fan-out implications
- A deduplication step applies a business priority rule

A one or two sentence comment at the model/task level is sufficient. Do not document the obvious.

---

## Naming as a lineage signal

Consistent naming conventions carry lineage information implicitly:

- `stg_<source>_<entity>` → this model cleans source data from `<source>`
- `mart_<domain>_<entity>` → this model applies business logic for `<domain>`
- `dim_<entity>` / `fact_<entity>` → dimensional layer, consumed by downstream reporting

A model name that follows layer conventions tells the reader where it sits in the pipeline without needing to open the file. Deviations from naming conventions break this implicit lineage signal.
