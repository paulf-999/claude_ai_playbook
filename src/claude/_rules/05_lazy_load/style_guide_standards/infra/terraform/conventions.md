# 🏷️ Conventions

Naming standards and declaration rules for Snowflake objects, Terraform resources, modules, variables, and outputs.

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
- [📋 Variable declaration requirements](#-variable-declaration-requirements)
- [✅ Validation blocks](#-validation-blocks)
- [📤 Output declarations](#-output-declarations)

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

---

## 📋 Variable declaration requirements

Every variable must declare all three of the following:

| Field | Requirement |
|-------|-------------|
| `description` | Always required — explain what the variable controls and any constraints |
| `type` | Always explicit — use `string`, `number`, `bool`, `list(...)`, `map(...)` as appropriate |
| `default` | Omit unless a safe default exists — prefer requiring callers to be explicit |

Mark variables that contain credentials or sensitive values with `sensitive = true`.

---

## ✅ Validation blocks

Use `validation` blocks to enforce naming conventions and format constraints at the variable level, rather than failing silently at apply time.

```terraform
variable "name" {
  description = <<-EOT
    Snowflake role name. Must match:
      - Prefix: one of ACCESS_, PRIV_, FUNC_, PRD_, CICD_, UAT_, DTE_, OWNER_
      - Suffix: one of _ALL_ROLE, _SEL_ROLE, _ROLE
      - Middle section: only uppercase A–Z and underscores (no numbers)
      - Max length 255
  EOT
  type = string

  validation {
    condition = can(regex(
      "^(ACCESS|PRIV|FUNC|PRD|CICD|UAT|DTE|OWNER)_[A-Z_]+(_ALL_ROLE|_SEL_ROLE|_ROLE)$",
      var.name
    ))
    error_message = "Role name must match pattern (uppercase letters and underscores only)."
  }

  validation {
    condition     = length(var.name) <= 255
    error_message = "Role name must be 255 characters or fewer."
  }
}
```

- Write one `validation` block per constraint — do not combine unrelated conditions.
- `error_message` must describe what a valid value looks like.
- Use `<<-EOT` heredoc syntax for multi-line descriptions.

---

## 📤 Output declarations

Every output must include a `description`. Reference the resource attribute directly — do not compute values in output blocks.

```terraform
output "name" {
  description = "The Snowflake role name."
  value       = snowflake_account_role.this.name
}
```

Expose only the attributes that callers are expected to consume.
