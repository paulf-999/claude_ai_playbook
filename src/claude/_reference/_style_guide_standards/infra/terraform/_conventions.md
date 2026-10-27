<!-- version: 2.0.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-27 -->
# 🏷️ Conventions

**Purpose:** Set naming standards for Snowflake objects, Terraform resources, modules, variables and outputs; declaration rules live in [`_declarations.md`](_declarations.md).

## ❄️ Snowflake object names

Snowflake objects are UPPER_CASE. Naming patterns are enforced via `validation` blocks on the corresponding input variable.

### Roles

```
<PREFIX>_<NAME>_<SUFFIX>
```

| Component | Allowed values |
|-----------|---------------|
| Prefix | `ACCESS`, `PRIV`, `FUNC`, `PRD`, `CICD`, `UAT`, `DTE`, `OWNER` |
| Name | Uppercase letters and underscores only — no numbers |
| Suffix | `_ALL_ROLE`, `_SEL_ROLE`, `_ROLE` |

Examples: `FUNC_CREATE_MODIFY_DATABASE_ROLE`, `ACCESS_READ_ONLY_ROLE`

### Warehouses

Pattern: `<NAME>_WH` — e.g. `DEV_WH`, `APP_DB_FILE_SUBMITTER_WH`

## 📋 Contents

- [🔧 Terraform resource names](#-terraform-resource-names)
- [📦 Module names](#-module-names)
- [📥 Variable names](#-variable-names)
- [📤 Output names](#-output-names)

---

## 🔧 Terraform resource names

| Construct | Convention | Example |
|-----------|------------|---------|
| Primary resource in a module | `this` | `resource "snowflake_account_role" "this"` |
| Non-primary resources | Descriptive `snake_case` prefixed with purpose | `module_grant_ownership_snowflake_warehouse` |

Use `this` when a module manages a single primary resource. Name each resource descriptively when a module creates multiple related resources.

---

## 📦 Module names

| Convention | Example |
|------------|---------|
| Reusable module directories: `snake_case` | `snowflake_role`, `grants_db_access` |
| Environment sub-module directories: numbered `snake_case` | `1_roles_and_grants` |
| Module block labels in HCL: `snake_case` | `module "roles_and_grants"` |

---

## 📥 Variable names

| Category | Convention | Example |
|----------|------------|---------|
| Provider / authentication variables | `SCREAMING_SNAKE_CASE` | `SNOWFLAKE_ORGANIZATION_NAME` |
| All other input variables | `snake_case` | `sf_warehouse_name`, `role_name_ownership_perms` |

---

## 📤 Output names

Use `snake_case`, named to describe the value they expose — not the resource they come from.

Examples: `name`, `id`, `dq_framework_db`
