# ✅ Data Validation

## Two layers of validation

Schema validity and data validity are distinct checks — both are required:

| Layer | Question | When to check |
|---|---|---|
| **Schema validation** | Are the expected columns present with the right types and nullability? | At the pipeline boundary, before processing |
| **Data validation** | Do the values conform to domain rules and business logic? | At the source boundary and between pipeline stages |

A source that passes schema validation can still contain logically corrupt data. A structurally correct file with negative transaction amounts or future-dated records will propagate silently downstream if only schema is checked.

---

## Schema boundary validation

Before processing a new batch of data, validate at the ingestion boundary:

- Expected columns are present (fail fast on missing required columns)
- Data types match expectations (a string where a number is expected will cause downstream failures)
- Non-nullable fields are populated (nulls in required fields should be caught here, not in dbt tests downstream)
- No unexpected columns that might indicate a schema version change

Do not rely on downstream dbt tests to catch ingestion schema drift — by the time a dbt test fails, the corrupt data is already in the warehouse.

---

## Business-rule validation

Domain rules define what valid data looks like for a specific source. Apply these checks before the data enters the main pipeline:

Common categories:
- **Range checks**: amounts must be positive; percentages between 0 and 100; dates not in the future
- **Referential integrity**: foreign keys must resolve to known entities (merchant IDs, transaction IDs)
- **Uniqueness**: primary keys must be unique within a batch
- **Completeness**: required combinations of fields must be co-present

---

## Reject vs quarantine

When records fail validation, choose a handling strategy and document it:

| Strategy | Use when |
|---|---|
| **Reject** (fail the pipeline) | Any invalid record is unacceptable; downstream correctness depends on full integrity |
| **Quarantine** (route to error table) | Some invalid records are tolerable; valid records should still be processed; invalid records need investigation |
| **Warn and continue** | Minor anomalies that do not affect downstream correctness; log and monitor trend |

The strategy must be documented in the pipeline config or model comment — do not leave it implicit. A quarantine table with no owner or review process becomes a graveyard.
