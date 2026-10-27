<!-- version: 2.0.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-27 -->
# 📁 Structure

Directory layout, standard file conventions and what stays out of version control; provider configuration lives in [`providers.md`](providers.md).

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
