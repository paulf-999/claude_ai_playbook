# 📥 Variables & Outputs

Standards for declaring input variables, writing validation blocks, and defining outputs.

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

Rules for validation blocks:
- Apply at minimum format validation (regex) and length validation for all Snowflake object name variables.
- Write one `validation` block per constraint — do not combine unrelated conditions.
- `error_message` must describe what a valid value looks like, not just that the value is invalid.
- Use `<<-EOT` heredoc syntax for multi-line descriptions.

---

## 📤 Output declarations

Every output must include a `description`. Reference the resource attribute directly — do not compute values in output blocks.

```terraform
output "name" {
  description = "The Snowflake role name."
  value       = snowflake_account_role.this.name
}

output "id" {
  description = "The Snowflake role ID."
  value       = snowflake_account_role.this.id
}
```

- Output names use `snake_case` (see [naming_conventions.md](naming_conventions.md)).
- Expose only the attributes that callers are expected to consume — do not expose every attribute of every resource.
