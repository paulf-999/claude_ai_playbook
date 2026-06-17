# 🔁 Data Pipeline Style Guide

Generic, tool-agnostic patterns for data pipeline development. These patterns apply across Airflow DAGs, dbt models, and bespoke SQL pipelines. For tool-specific standards, see [`airflow.md`](airflow.md), [`dbt.md`](dbt.md), and [`sql.md`](sql.md).

For the normative rules underpinning these patterns, see `rules/development.md` (idempotency, incremental processing, partitioning, lineage, monitoring, cost optimisation).

---

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`data_pipeline/incremental_processing.md`](data_pipeline/incremental_processing.md) | When to use incremental vs full refresh; watermark patterns; late-arriving data |
| [`data_pipeline/partitioning.md`](data_pipeline/partitioning.md) | Partition key selection; granularity; filter alignment |
| [`data_pipeline/lineage.md`](data_pipeline/lineage.md) | Traceability requirements; dependency documentation conventions |
| [`data_pipeline/monitoring.md`](data_pipeline/monitoring.md) | Freshness SLAs; threshold alerting; silent failure detection |
| [`data_pipeline/data_validation.md`](data_pipeline/data_validation.md) | Schema boundary validation; business-rule validation; two-layer model |
| [`data_pipeline/cost_management.md`](data_pipeline/cost_management.md) | Materialisation tradeoffs; compute sizing; full refresh cost scaling |

---

## 📥 Imports

@./data_pipeline/incremental_processing.md
@./data_pipeline/partitioning.md
@./data_pipeline/lineage.md
@./data_pipeline/monitoring.md
@./data_pipeline/data_validation.md
@./data_pipeline/cost_management.md
