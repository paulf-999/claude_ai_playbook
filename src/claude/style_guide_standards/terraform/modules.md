# 📦 Modules

Standards for module composition, provider passing, iteration patterns, and lifecycle management.

## 🧩 Module composition pattern

Environment root modules call reusable child modules. Outputs from one module are passed as inputs to dependent modules — never hardcode values that another module has already computed.

```terraform
module "roles_and_grants" {
  source    = "./1_roles_and_grants"
  providers = { snowflake = snowflake }

  db_name_dq_framework_db = module.dq_framework_db.dq_framework_db
  db_name_operations_db   = module.operations_db.operations_db
}
```

- Always pass providers explicitly using the `providers` argument — do not rely on implicit provider inheritance.
- Use relative paths for module sources within the same repository (`source = "../../grants/default_grants_new_role_v1"`).

---

## 🔁 Layered resource pattern

Within a module, follow the create → ownership → usage pattern for Snowflake resources:

```terraform
# 1. Create the resource
resource "snowflake_warehouse" "this" { ... }

# 2. Grant OWNERSHIP to the owning role
resource "snowflake_grant_ownership" "module_grant_ownership_snowflake_warehouse" { ... }

# 3. Grant USAGE to consumer roles
resource "snowflake_grant_privileges_to_account_role" "module_grant_usage_snowflake_warehouse" { ... }
```

This pattern keeps permission management co-located with the resource it governs.

---

## 🔄 Iteration with for_each

Use `for_each` to create multiple instances of a resource from a set or map. Prefer `toset()` when iterating over a list of strings.

```terraform
resource "snowflake_grant_account_role" "module_grant_role_to_system_roles" {
  for_each         = toset(local.system_roles)
  role_name        = var.role_name
  parent_role_name = each.value
}
```

- Use `each.key` and `each.value` — do not use `count` with lists, as `for_each` produces stable resource addresses.
- Define the iterable as a `local` where the source list needs transformation before use.

---

## ⚙️ Lifecycle management

Use `lifecycle` blocks to prevent Terraform from making unnecessary changes to resources where drift is expected or acceptable:

```terraform
resource "snowflake_grant_privileges_to_account_role" "example" {
  # ...
  lifecycle {
    ignore_changes = [privileges]
  }
}
```

- Document why `ignore_changes` is used in a comment — it should be an intentional decision, not a workaround.
- Do not use `prevent_destroy = true` without team discussion, as it blocks environment teardown.

---

## 📝 Module README

Every module must have a `README.md` documenting:
- What the module creates
- All input variables and their constraints
- All outputs
- A usage example
