# 🏗️ Terraform Style Guide & Standards

Defines the team's standards for writing and structuring Terraform code, based on the `payroc/dmt-iac-snowflake_terraform` repository.

---

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`terraform/structure.md`](terraform/structure.md) | Directory layout and standard file conventions per module and environment |
| [`terraform/naming_conventions.md`](terraform/naming_conventions.md) | Snowflake object naming, Terraform resource names, and module names |
| [`terraform/variables_and_outputs.md`](terraform/variables_and_outputs.md) | Variable typing, descriptions, validation blocks, and output conventions |
| [`terraform/providers_and_versions.md`](terraform/providers_and_versions.md) | Provider configuration, version pinning, and authentication |
| [`terraform/modules.md`](terraform/modules.md) | Module composition, numbered ordering, provider passing, and iteration patterns |
| [`terraform/ci_and_tooling.md`](terraform/ci_and_tooling.md) | Pre-commit hooks, Azure Pipelines, and sequential environment deployment |

---

## 🏗️ Core principles

- **Separation by environment** — each environment (`dev`, `uat`, `cicd`, `prod`, `global`) is an independent Terraform root module with its own state.
- **Modules for reuse** — shared resource patterns (roles, warehouses, grants) live in `terraform/modules/` and are called from environment configurations.
- **Config-driven** — no credentials or environment-specific values are hardcoded. Use `.env_template` to guide local setup and Airflow Variables/Connections for runtime values.
- **Validation-first** — variable inputs are validated with `validation` blocks; naming conventions for Snowflake objects are enforced at the variable level.
- **Minimal DAG code in Terraform** — Terraform manages Snowflake infrastructure (roles, warehouses, databases, grants), not application logic.

---

## 📥 Imports

@./terraform/structure.md
@./terraform/naming_conventions.md
@./terraform/variables_and_outputs.md
@./terraform/providers_and_versions.md
@./terraform/modules.md
@./terraform/ci_and_tooling.md
