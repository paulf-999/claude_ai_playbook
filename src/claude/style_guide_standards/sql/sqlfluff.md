# 🔧 SQLFluff Configuration

SQL style is enforced by SQLFluff. The canonical config lives in the dbt repo:
[`da-etl-dbtanalytics/.sqlfluff`](https://github.com/payroc/da-etl-dbtanalytics/blob/main/.sqlfluff)

All SQLFluff violations must be resolved before committing.

---

## 🗣️ Dialect and templater

- Dialect: `snowflake`
- Templater: `dbt`
- Max line length: 120 characters

---

## 🚫 Excluded rules

The following SQLFluff rules are excluded in the team config, with reasons:

| Rule | Reason |
|---|---|
| L027 | References with mixed qualification allowed |
| L029 | Keywords permitted as column names (legacy code) |
| L033 | `UNION ALL` vs `UNION` not enforced |
| L034 | Column reordering not enforced (preserves author intent) |
| L057 | Special characters in column names allowed (source data) |
| L059 | Unnecessary quoting not enforced |
| LT15 | Consecutive blank lines around CTEs not enforced |
| ST09 | Join clause ordering not enforced |
