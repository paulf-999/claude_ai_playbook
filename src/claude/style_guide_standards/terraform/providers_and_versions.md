# 🔌 Providers & Versions

Standards for provider configuration, version pinning, authentication, and Terraform version requirements.

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

- `required_version`: Set to `>= 1.0.0` as the minimum — update as the team upgrades.
- Provider version: Pin to the exact version agreed for the environment. Upgrading a provider version requires a deliberate change, not an implicit one.
- Commit `.terraform.lock.hcl` to version control — it records the exact provider version resolved and must be consistent across the team.

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
- The private key is read from the local filesystem via `file()` — the path `~/.ssh/snowflake_key.p8` is the team standard. Do not commit the key file.
- See `.env_template` in each environment directory for the expected environment variable names.

---

## 🔬 Preview features

When a resource type requires preview feature enablement, declare it explicitly in the provider block:

```terraform
provider "snowflake" {
  # ... authentication config above ...

  preview_features_enabled = [
    "snowflake_table_resource",
    "snowflake_table_constraint_resource",
  ]
}
```

- Only enable the specific preview features required — do not enable all.
- Document in `README.md` when a module relies on a preview feature, as it may affect provider upgrade compatibility.
