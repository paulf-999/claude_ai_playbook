# 🔁 CI & Tooling

Standards for pre-commit hooks, code formatting, and the Azure Pipelines CI/CD workflow.

## 🪝 Pre-commit hooks

The following hooks are enforced on every commit via `.pre-commit-config.yaml`:

| Hook | Purpose |
|------|---------|
| `no-commit-to-branch` (main) | Prevents direct commits to the `main` branch |
| `check-merge-conflict` | Rejects files containing merge conflict markers |
| `end-of-file-fixer` | Ensures all files end with a single newline |
| `trailing-whitespace` | Removes trailing whitespace |
| `detect-private-key` | Blocks commits containing private key material |
| `terraform_fmt` | Runs `terraform fmt` on all `.tf` files |
| `yamllint` | Lints YAML files against `.yamllint` config (120-char line limit) |
| `yamlfmt` | Formats YAML files consistently |

All hooks must pass before a commit is accepted. Do not suppress failures without a documented reason.

---

## 🎨 Terraform formatting

Run `terraform fmt -recursive` before committing to ensure consistent formatting across all `.tf` files. The `terraform_fmt` pre-commit hook enforces this automatically.

Key formatting rules enforced by `terraform fmt`:
- Align `=` signs within blocks.
- Indent with 2 spaces.
- One blank line between resource blocks.

---

## 🚀 Azure Pipelines — PR validation

On every pull request, the pipeline runs `terraform validate` and `terraform plan` across all environments:

```
DEV → UAT → CICD → PROD → GLOBAL  (all in parallel on PR)
```

The PR pipeline uses a shared template: `src/cicd/pipelines/pr_pipeline_terraform_validate_and_plan.yml`.

No PR may be merged if any environment's `validate` or `plan` step fails.

---

## 🚀 Azure Pipelines — deployment

On merge to `main`, Terraform is applied to each environment in sequence:

```
DEV → UAT → CICD → PROD → GLOBAL
```

Each environment's apply job depends on the previous one completing successfully (`dependsOn`). A failure in `dev` blocks all downstream environments.

The deployment pipeline uses a shared template: `src/cicd/pipelines/code_deployment_terraform_apply.yml`.

Secrets are retrieved from Azure Key Vault at runtime — they are not stored in pipeline variables or code.
