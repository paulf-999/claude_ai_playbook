# 💸 Pipeline Cost Management

## Materialisation tradeoff framework

Choosing the wrong materialisation is the most common source of avoidable pipeline cost:

| Materialisation | Write cost | Query cost | Use when |
|---|---|---|---|
| **View** | None | Paid at query time (full recompute) | Lightweight transformations queried infrequently; logic that must always reflect the latest source data |
| **Table** | Paid at build time | Low (reads pre-computed data) | Expensive transformations queried frequently; downstream models that join to this model |
| **Incremental** | Paid on delta only | Low | Large tables that grow continuously; same conditions as table but where full refresh cost is unacceptable |
| **Ephemeral** | None (inlined into parent) | Paid in parent query | Simple intermediate logic with a single consumer; not appropriate if used by multiple downstream models |

Default to `incremental` for tables expected to exceed ~50M rows. A full-refresh table model that was acceptable at launch often becomes the largest line item in the warehouse bill as data accumulates.

---

## Right-sizing compute

Snowflake warehouse cost scales with size and runtime. Two common failure modes:

1. **Oversized warehouse**: using XL when S would meet the SLA — common when a warehouse was scaled up for a one-off task and never scaled back down
2. **Undersized warehouse**: a pipeline that consistently spills to disk or queues tasks is costing more in wall-clock time than a larger warehouse would cost in credits

Guidelines:
- Start at the smallest warehouse that meets the SLA; scale up only if the SLA is breached
- Configure `AUTO_SUSPEND` on all warehouses (60 seconds is a reasonable default for pipeline warehouses)
- Do not share a pipeline warehouse with interactive/BI query traffic — contention degrades both and obscures cost attribution

---

## Full refresh cost scaling

Compute cost for a full refresh scales with table size. Before choosing full refresh:

| Table size | Consideration |
|---|---|
| < 10M rows | Full refresh is usually fine |
| 10M–100M rows | Evaluate incremental; full refresh acceptable if load is infrequent |
| > 100M rows | Incremental required unless there is a documented reason (e.g. source data is mutable without a reliable change indicator) |

If a full refresh is genuinely required, document why in the model or pipeline config — a future engineer should not have to reverse-engineer the decision.

---

## Query attribution

Use Snowflake query tags to attribute compute cost to the owning pipeline or model. This makes it possible to identify the most expensive pipelines and prioritise optimisation work.

Set query tags at the session level in Airflow operators and dbt model configs — see `rules/development.md` (Logging and observability) for the requirement.
