<!-- version: 1.0.0 -->
<!-- created: 2026-10-27 -->
<!-- updated: 2026-10-27 -->
# 📋 Declarations

What every variable and output must declare, and how to validate inputs, split from [`conventions.md`](conventions.md).

## 📋 Contents

- [📋 Variable declaration requirements](#-variable-declaration-requirements)
- [✅ Validation blocks](#-validation-blocks)
- [📤 Output declarations](#-output-declarations)

---

## 📋 Variable declaration requirements

Every variable must declare `description` and `type`, and declares `default` only when a safe one exists:

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
