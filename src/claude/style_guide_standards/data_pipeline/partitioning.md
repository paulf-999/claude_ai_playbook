# 🗂️ Data Partitioning

## Partition key selection

A good partition key dramatically reduces the data scanned per query. Choose based on:

| Criterion | Guidance |
|---|---|
| **Query filter frequency** | The key must appear in `WHERE` clauses on the majority of queries — no benefit if rarely filtered |
| **Cardinality** | High enough to create meaningful partitions (date, merchant_id) — not so high that each partition is trivially small |
| **Data distribution** | Avoid skewed keys where one value dominates (e.g. a status field that is 99% `active`) |
| **Write pattern** | For append-only data, time-based keys align naturally with write windows |

Most pipelines should partition on a **time column** (`created_date`, `event_date`, `load_date`). Add a secondary clustering key (merchant ID, entity ID) if queries consistently filter on both.

---

## Partition granularity

| Granularity | Use when |
|---|---|
| Day | Standard for transactional and event data; good balance of partition count and scan reduction |
| Month | Appropriate for slowly-changing dimensional data or aggregated summaries |
| Year | Only for very low-volume historical data; rarely appropriate for operational tables |

Prefer day-level granularity unless partition management overhead (too many partitions) is a real concern at the data volume in question.

---

## Filter alignment

Partitioning only reduces scan cost if query filters align with the partition key:

- Use `DATE_TRUNC('day', event_time)` rather than `CAST(event_time AS DATE)` when the partition key was defined with `DATE_TRUNC` — mismatched expressions prevent partition pruning
- Push partition filter conditions as early as possible in the query — before joins, not after
- In incremental models, the partition filter in the `WHERE` clause must reference the same expression used to define the clustering key

Verify pruning is happening: check the `Partitions scanned` stat in Snowflake's Query Profile after adding a new clustering key.

---

## When not to partition

- Small tables (< ~10M rows) — partition overhead outweighs the scan savings; a full scan is fast enough
- Tables with uniform query patterns that scan all data (e.g. a full aggregate over all time) — no benefit
- Reference / lookup tables — these are typically small, rarely benefit from partitioning, and add join complexity
