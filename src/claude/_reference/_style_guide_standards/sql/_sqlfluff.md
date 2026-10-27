<!-- version: 1.1.1 -->
<!-- created: 2026-04-08 -->
<!-- updated: 2026-10-27 -->
# 🔧 SQLFluff Configuration

**Purpose:** Record the team's SQLFluff settings and excluded rules, so every SQL file is checked the same way.

SQL style is enforced by SQLFluff. The canonical config lives in the dbt repo:
the dbt project's `.sqlfluff`

All SQLFluff violations must be resolved before committing.

## 🗣️ Dialect and templater

- Dialect: `snowflake`
- Templater: `dbt`
- Max line length: 120 characters

---

## 🚫 Excluded rules

The following SQLFluff rules are excluded in the team config, with reasons. Codes use SQLFluff 2.0+ names, and the legacy code in brackets is the alias older configs may still use:

| Rule | What it checks | Why it's excluded |
|---|---|---|
| `RF02` (`L027`) | Columns are qualified when a query reads from more than one table | Not enforced by lint, though `_formatting.md` still asks for table prefixes in joins |
| `RF04` (`L029`) | Unreserved keywords aren't used as identifiers | Legacy column names use them |
| `AM02` (`L033`) | `UNION` is written as `UNION ALL` or `UNION DISTINCT` | Bare `UNION` is allowed |
| `ST06` (`L034`) | Wildcards and simple columns come before calculations in `SELECT` | Preserves the author's column order |
| `RF05` (`L057`) | Identifiers contain no special characters | Source data has them |
| `RF06` (`L059`) | Identifiers aren't quoted unnecessarily | Unnecessary quoting is allowed |
| `LT15` | No run of too many blank lines | Extra blank lines between CTEs are allowed |
| `ST09` | Join conditions list the earlier table first | Join condition order is not enforced |
