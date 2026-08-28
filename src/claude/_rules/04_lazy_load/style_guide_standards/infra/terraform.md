# 🏗️ Terraform Style Guide & Standards

Defines the team's standards for writing and structuring Terraform code.

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`terraform/structure.md`](terraform/structure.md) | Directory layout, standard files, provider configuration, and version pinning |
| [`terraform/conventions.md`](terraform/conventions.md) | Snowflake object naming, resource names, variable declarations, and outputs |
| [`terraform/modules.md`](terraform/modules.md) | Module composition, layered resource pattern, iteration, and lifecycle |
| [`terraform/ci_and_tooling.md`](terraform/ci_and_tooling.md) | Pre-commit hooks, Azure Pipelines, and sequential environment deployment |

## 📋 Contents

- [🏗️ Core principles](#-core-principles)

---

## 🏗️ Core principles

- **Separation by environment** — each environment (`dev`, `uat`, `cicd`, `prod`, `global`) is an independent Terraform root module with its own state.
- **Modules for reuse** — shared resource patterns (roles, warehouses, grants) live in `terraform/modules/` and are called from environment configurations.
- **Config-driven** — no credentials or environment-specific values are hardcoded; use `.env_template` to guide local setup.
- **Validation-first** — variable inputs are validated with `validation` blocks; naming conventions for Snowflake objects are enforced at the variable level.
- **Infrastructure only** — Terraform manages Snowflake infrastructure (roles, warehouses, databases, grants), not application logic.
