---
paths:
  - "**/*.tf"
---
<!-- version: 1.2.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-27 -->
<!-- miss_cost: medium — modules that fail review or plan checks -->
<!-- loading: path-scoped — only applies to Terraform, so it loads when a .tf file is open -->
# 🏗️ Terraform Style Guide & Standards

**Purpose:** Define the team's standards for writing and structuring Terraform code.

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`terraform/_structure.md`](terraform/_structure.md) | Directory layout, standard files, and what must not be committed |
| [`terraform/_providers.md`](terraform/_providers.md) | Provider version pinning, authentication, and preview features |
| [`terraform/_conventions.md`](terraform/_conventions.md) | Snowflake object naming, and resource, module, variable and output names |
| [`terraform/_declarations.md`](terraform/_declarations.md) | Variable and output declaration rules, and validation blocks |
| [`terraform/_modules.md`](terraform/_modules.md) | Module composition, layered resource pattern, iteration, and lifecycle |
| [`terraform/_ci_and_tooling.md`](terraform/_ci_and_tooling.md) | Pre-commit hooks, Azure Pipelines, and sequential environment deployment |

## 🏗️ Core principles

- **Separation by environment** — each environment (`dev`, `uat`, `cicd`, `prod`, `global`) is an independent Terraform root module with its own state.
- **Modules for reuse** — shared resource patterns (roles, warehouses, grants) live in `terraform/modules/` and are called from environment configurations.
- **Config-driven** — no credentials or environment-specific values are hardcoded; use `.env_template` to guide local setup.
- **Validation-first** — variable inputs are validated with `validation` blocks; naming conventions for Snowflake objects are enforced at the variable level.
- **Infrastructure only** — Terraform manages Snowflake infrastructure (roles, warehouses, databases, grants), not application logic.
