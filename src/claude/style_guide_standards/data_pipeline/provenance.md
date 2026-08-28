# 🧾 Provenance Footers

## Why provenance footers

Any answer derived from data carries an implicit trust claim. A number without a stated source,
freshness, or owner asks the reader to trust it blindly. A provenance footer makes that trust
claim explicit and cheap to verify — without requiring the heavier validation machinery (evals,
adversarial review) that governs the data itself.

Any Claude skill or response that answers a data question with a number, finding, or metric
derived from the warehouse must end with a provenance footer.

---

## Required fields

| Field | Content |
|---|---|
| **Source tier** | Where the number came from, in trust order (see below) |
| **Data freshness** | As-of timestamp of the query, or the last successful dbt run for the model queried |
| **Model owner** | The team or individual accountable for the source model — from `dbt` model `meta` / `group` config, or the relevant `CODEOWNERS` entry |

---

## Source tier trust order

State the tier explicitly — do not just name the object queried:

1. **Governed metric / semantic layer** — a defined metric or semantic model (highest trust; business logic is centrally maintained and tested)
2. **Curated dbt model** — a `mart` or `warehouse` layer model (tested, documented, follows `ref()` lineage)
3. **Raw table** — a `staging` model or raw source table queried directly (lowest trust; no business logic applied, may not reflect current definitions)

If a query spans multiple tiers (e.g. joins a mart model to a raw table), state the lowest tier present — the footer's trust claim is only as strong as its weakest input.

---

## Worked example

```
---
Source tier:     Curated dbt model (mart.fct_merchant_transactions)
Data freshness:  Last dbt run succeeded 2026-07-03T06:12:00Z (daily schedule)
Model owner:     Data Platform Engineering (see dbt meta.owner)
```

---

## When a footer is not required

- Responses that do not state a data-derived number, finding, or metric (e.g. explaining how a
  model works, planning a schema change)
- Intermediate progress narration within a multi-phase skill — the footer belongs on the final
  answer, not every step
