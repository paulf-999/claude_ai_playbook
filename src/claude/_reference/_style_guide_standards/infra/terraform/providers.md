<!-- version: 1.0.0 -->
<!-- created: 2026-10-27 -->
<!-- updated: 2026-10-27 -->
# 🔌 Providers

Provider version pinning, authentication and preview features, split from [`structure.md`](structure.md).

## 📋 Contents

- [🔒 Version pinning](#-version-pinning)
- [🔑 Provider authentication](#-provider-authentication)
- [🔬 Preview features](#-preview-features)

---

## 🔒 Version pinning

Pin the Snowflake provider to an **exact version** in all environment root modules. Do not use range constraints (`~>`, `>=`) in environments — only in module `provider.tf` files where caller flexibility is needed.

```terraform
terraform {
  required_version = ">= 1.0.0"

  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "2.5.0"
    }
  }
}
```

- Commit `.terraform.lock.hcl` to version control — it records the exact provider version resolved and must be consistent across the team.
- Upgrading a provider version requires a deliberate change, not an implicit one.

---

## 🔑 Provider authentication

Authentication uses JWT via a private key file — not username/password.

```terraform
provider "snowflake" {
  organization_name = var.SNOWFLAKE_ORGANIZATION_NAME
  account_name      = var.SNOWFLAKE_ACCOUNT_NAME
  user              = var.SNOWFLAKE_USER
  private_key       = file("~/.ssh/snowflake_key.p8")
  authenticator     = "SNOWFLAKE_JWT"
  role              = var.SNOWFLAKE_ROLE
  warehouse         = var.SNOWFLAKE_WAREHOUSE
}
```

- All authentication values are passed in as variables — never hardcoded.
- The private key path `~/.ssh/snowflake_key.p8` is the team standard — do not commit the key file.
- See `.env_template` in each environment directory for the expected environment variable names.

---

## 🔬 Preview features

When a resource type requires preview feature enablement, declare it explicitly in the provider block and document it in `README.md` — preview features may affect provider upgrade compatibility.

```terraform
provider "snowflake" {
  preview_features_enabled = [
    "snowflake_table_resource",
  ]
}
```

Only enable the specific preview features required — do not enable all.
