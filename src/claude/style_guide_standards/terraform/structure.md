# 📁 Directory & File Structure

Standards for how Terraform code is organised across environments, modules, and examples.

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
    └── modules/
        ├── snowflake_role/
        └── snowflake_service_user/
```

---

## 📄 Standard files per module or environment

Every module and every environment root must contain these files:

| File | Purpose |
|------|---------|
| `main.tf` | Resource definitions or module calls |
| `variables.tf` | Input variable declarations with types, descriptions, and validation |
| `outputs.tf` | Output value declarations |
| `provider.tf` | Provider and Terraform version requirements |
| `README.md` | Module documentation — purpose, inputs, outputs, example usage |

Optional files present in some modules or environments:

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

The number prefix signals the intended execution order — lower numbers must be applied before higher numbers. Do not rely on implicit ordering.

---

## 🔒 What must not be committed

- `.env` files — use `.env_template` to document required variables
- `terraform.tfstate` and `terraform.tfstate.backup` — state must be stored remotely
- Private keys or credentials of any kind
- The `detect-private-key` pre-commit hook enforces this automatically
