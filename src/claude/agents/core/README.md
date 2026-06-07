# 🎭 Agents — Core

Full-session personas and data pipeline specialists. General-purpose personas are used for open-ended sessions; pipeline specialists are dispatched by skills (`/review_dbt_pr`, `/new_dbt_warehouse_project`) and cover specific stages of the data delivery lifecycle.

## General-purpose personas

| File | Agent name | Purpose |
|------|------------|---------|
| [`architect.md`](architect.md) | `architect` | 🏛️ End-to-end analytics architecture, hands-on across the full stack *(default)* |
| [`project_manager.md`](project_manager.md) | `project_manager` | 📋 Work planning, task structuring, documentation, and stakeholder communication |
| [`technical_writer.md`](technical_writer.md) | `technical_writer` | ✍️ Draft and improve documentation, READMEs, runbooks, ADRs, and Confluence pages |

## Data pipeline specialists

Dispatched by skills (`/review_dbt_pr`, `/new_dbt_warehouse_project`). Each covers a specific stage of the data delivery lifecycle.

| File | Agent name | Purpose |
|------|------------|---------|
| [`data-project-manager.md`](data-project-manager.md) | `data-project-manager` | 🗂️ Orchestrates end-to-end data pipeline delivery from brief to sign-off |
| [`requirements-consolidator.md`](requirements-consolidator.md) | `requirements-consolidator` | 📋 Consolidates business requirements into a structured technical brief |
| [`payroc-data-architect.md`](payroc-data-architect.md) | `payroc-data-architect` | 🏛️ Designs dbt data models and source-to-target mappings for the Payroc warehouse |
| [`dbt-warehouse-engineer.md`](dbt-warehouse-engineer.md) | `dbt-warehouse-engineer` | 🔧 Writes and refactors dbt SQL models following Payroc standards |
| [`dbt-pr-reviewer.md`](dbt-pr-reviewer.md) | `dbt-pr-reviewer` | 🔍 Reviews dbt PRs against coding standards and posts a formal GitHub review |
| [`dbt-uat-test-planner.md`](dbt-uat-test-planner.md) | `dbt-uat-test-planner` | 📝 Produces UAT testing plans for dbt PRs |
| [`dbt-uat-evaluator.md`](dbt-uat-evaluator.md) | `dbt-uat-evaluator` | ✅ Executes UAT validation queries and posts a GO/NO-GO evaluation report |
| [`data-docs-writer.md`](data-docs-writer.md) | `data-docs-writer` | ✍️ Writes data documentation — Confluence pages, dbt YAML descriptions, README files |
| [`airflow-dag-engineer.md`](airflow-dag-engineer.md) | `airflow-dag-engineer` | ⚙️ Writes and reviews Airflow DAGs following Payroc patterns |
| [`omni-semantic-engineer.md`](omni-semantic-engineer.md) | `omni-semantic-engineer` | 📊 Designs and updates the Omni semantic layer for the Payroc data platform |
