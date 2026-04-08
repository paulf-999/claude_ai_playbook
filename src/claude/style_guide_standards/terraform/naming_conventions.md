# 🏷️ Naming Conventions

Standards for naming Snowflake objects, Terraform resources, modules, variables, and outputs.

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

Examples: `FUNC_CREATE_MODIFY_DATABASE_ROLE`, `ACCESS_READ_ONLY_ROLE`, `DQ_ALL_ROLE`

### Warehouses

```
<NAME>_WH
```

Examples: `DEV_WH`, `APP_DB_FILE_SUBMITTER_WH`

---

## 🔧 Terraform resource names

| Construct | Convention | Example |
|-----------|------------|---------|
| Resource type | Provider-defined `snake_case` | `snowflake_account_role` |
| Primary resource in a module | `this` | `resource "snowflake_account_role" "this"` |
| Non-primary resources | Descriptive `snake_case` prefixed with purpose | `module_grant_ownership_snowflake_warehouse` |

Use `this` as the logical name when a module manages a single primary resource. For modules that create multiple related resources (e.g. the resource plus its grants), name each resource to describe its purpose clearly.

---

## 📦 Module names

| Convention | Example |
|------------|---------|
| Reusable module directories: `snake_case` | `snowflake_role`, `grants_db_access` |
| Environment sub-module directories: numbered `snake_case` | `1_roles_and_grants`, `2_account_level_objects` |
| Module block labels in HCL: `snake_case` describing the instance | `module "roles_and_grants"` |

---

## 📥 Variable names

Two distinct conventions apply depending on the purpose of the variable:

| Category | Convention | Example |
|----------|------------|---------|
| Provider / authentication variables | `SCREAMING_SNAKE_CASE` | `SNOWFLAKE_ORGANIZATION_NAME`, `SNOWFLAKE_USER` |
| All other input variables | `snake_case` | `sf_warehouse_name`, `role_name_ownership_perms` |

---

## 📤 Output names

Outputs use `snake_case` and are named to describe the value they expose, not the resource they come from:

| Convention | Example |
|------------|---------|
| `snake_case`, value-descriptive | `name`, `id`, `dq_framework_db` |
