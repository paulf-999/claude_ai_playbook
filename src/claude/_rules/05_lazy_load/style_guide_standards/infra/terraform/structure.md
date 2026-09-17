# 📁 Structure & Providers

Directory layout, standard file conventions, provider configuration, and version pinning.

## 🗂️ Top-level layout

```
terraform/
├── environments/         # Environment-specific root modules
│   ├── dev/
│   ├── uat/
│   ├── cicd/
│   ├── prod/
│   └── global/
├── modules/              # Reusable module definitions
│   ├── account_level_objects/
│   │   ├── snowflake_role/
│   │   ├── snowflake_service_user/
│   │   └── warehouse/
│   └── grants/
│       ├── default_grants_new_role_v1/
│       └── grants_db_access/
│           ├── grant_ownership_all_db_objects/
│           ├── grant_read_only_db_access/
│           └── grant_write_db_access/
└── examples/             # Standalone usage examples for modules
```

## 📋 Contents

- [📄 Standard files per module or environment](#-standard-files-per-module-or-environment)
- [🔢 Numbered subdirectory convention](#-numbered-subdirectory-convention)
- [🔒 What must not be committed](#-what-must-not-be-committed)
- [🔒 Version pinning](#-version-pinning)
- [🔑 Provider authentication](#-provider-authentication)
- [🔬 Preview features](#-preview-features)

---

## 📄 Standard files per module or environment

Every module and every environment root must contain:

| File | Purpose |
|------|---------|
| `main.tf` | Resource definitions or module calls |
| `variables.tf` | Input variable declarations with types, descriptions, and validation |
| `outputs.tf` | Output value declarations |
| `provider.tf` | Provider and Terraform version requirements |
| `README.md` | Module documentation — purpose, inputs, outputs, example usage |

Optional files:

| File | Purpose |
|------|---------|
| `.env_template` | Template listing the environment variables required for local runs |
| `local_terraform_dev.sh` | Shell script for local development setup |

---

## 🔢 Numbered subdirectory convention

Within an environment, sub-modules are numbered to make dependency order explicit:

```
environments/prod/
├── 1_roles_and_grants/
├── 2_account_level_objects/
└── ...
```

Lower numbers must be applied before higher numbers — do not rely on implicit ordering.

---

## 🔒 What must not be committed

- `.env` files — use `.env_template` to document required variables
- `terraform.tfstate` and `terraform.tfstate.backup` — state must be stored remotely
- Private keys or credentials of any kind
- The `detect-private-key` pre-commit hook enforces this automatically

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
