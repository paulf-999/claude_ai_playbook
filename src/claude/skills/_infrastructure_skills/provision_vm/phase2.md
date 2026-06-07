# 🖥️ Phase 2 — VM Config PR

**Goal:** Add Terraform configuration for the new VM under `envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>/`.

---

## 🔎 Step 2a — Verify workspace PR is merged

Check whether the workspace branch still exists on the remote:

```bash
git -C <REPO_PATH> ls-remote --heads origin feature/add_<WORKLOAD_DIR>_workspace
```

If the branch is still present, warn the user:

> "The workspace PR branch `feature/add_<WORKLOAD_DIR>_workspace` is still present on the
> remote — the PR may not have been merged yet. Proceeding now could cause Scalr to error.
> Confirm you want to continue anyway?"

Wait for explicit confirmation before proceeding.

Pull latest main:

```bash
git -C <REPO_PATH> checkout main
git -C <REPO_PATH> pull origin main
```

---

## 🗂️ Step 2b — Detect scenario: new directory vs existing directory

Check whether `<REPO_PATH>/envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>/` already exists.

### 📁 Scenario A — WORKLOAD_DIR does not exist (new VM, new directory)

1. List `<REPO_PATH>/envs/<ENV>/apps/<TIER>/`. Pick the alphabetically first existing
   sibling directory as the template source.

2. Read all `.tf` files in the template directory to:
   - Confirm `secrets.tf`, `variables.tf`, `versions.tf` are present.
   - Extract `golden_image_version` from the instance file — use this value in the
     generated file.
   - Note the instance file naming convention (e.g. `instance_<suffix>.tf`).

3. Proceed to Step 2c — full directory creation path.

### 📂 Scenario B — WORKLOAD_DIR already exists (adding a second instance to existing dir)

1. Read ALL `instance_*.tf` files in `<REPO_PATH>/envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>/`.

2. Extract:
   - Whether `module "compute"` is declared in any of them (if yes, **omit** from the new
     file — only one `module "compute"` block is allowed per directory).
   - All existing `module "instance_..."` block names — surface these to the user so they
     can confirm the new module name is unique.
   - All existing `instance_*.tf` filenames — surface these so the user can follow the
     same abbreviation convention (e.g. `instance_dbt.tf` → `instance_abt.tf`, not
     `instance_airbyte.tf`).
   - Extract `golden_image_version` from an existing instance file.

3. Show the user:
   > "Existing instance files in `<WORKLOAD_DIR>/`: `instance_dbt.tf`
   > Existing module names: `module "instance_dmws_dbt"`
   > `module "compute"` is already declared — it will be omitted from the new file."

4. Proceed to Step 2c — instance file only path (skip boilerplate copy).

---

## ⚙️ Step 2c — Generate the instance file

The instance file is named `instance_<INSTANCE_SUFFIX>.tf`.

**Include `module "compute"` only if Scenario A (new directory), or if Scenario B and no
existing `module "compute"` was found.**

```hcl
# Include only when module "compute" is not already declared in this directory:
module "compute" {
  source = "../../../../../modules/payroc/compute"
}

module "instance_<APPLICATION_OWNER>_<ASSET_ROLE>" {
  source = "../../../../../modules/payroc/primitives/virtual_machine"

  # These are passed in via variables.tf (no change needed here)
  site        = var.site
  environment = var.environment
  pci_scope   = var.pci_scope

  # Ownership / tagging
  application_owner = "<APPLICATION_OWNER>"
  asset_role        = "<ASSET_ROLE>"

  # OS details (usually unchanged unless targeting a different build)
  os                   = "<os>"
  os_edition           = "<os_edition>"
  os_version           = "<os_version>"
  golden_image_version = "<golden_image_version>"

  # Compute sizing: see modules/payroc/compute/compute_resources.tf
  compute_resources     = module.compute.<COMPUTE_RESOURCES>
  compute_workload_type = module.payroc_standards.compute_workloads.virtual_machine

  # Network / domain
  dns_servers        = var.dns_servers
  domain             = var.domain
  disks              = <DISKS>
  network_interfaces = [{ network_segment = "flat", use_dhcp = true }]
  patch_group        = "<PATCH_GROUP>"
  sequential_index   = "<SEQUENTIAL_INDEX>"
}
```

Note: `module "payroc_standards"` is declared in `variables.tf` — do **not** include it in
the instance file.

---

## 👀 Step 2d — Show proposed changes and confirm

### Scenario A (new directory):

```
New directory: envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>/
  secrets.tf                    — copied verbatim from <TEMPLATE_DIR>/secrets.tf
  variables.tf                  — copied verbatim from <TEMPLATE_DIR>/variables.tf
  versions.tf                   — copied verbatim from <TEMPLATE_DIR>/versions.tf
  instance_<INSTANCE_SUFFIX>.tf — new (generated — see content above)
```

### Scenario B (existing directory):

```
Existing directory: envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>/
  instance_<INSTANCE_SUFFIX>.tf — new (generated — see content above)
  [secrets.tf / variables.tf / versions.tf left unchanged]
```

Show the full generated instance file. Ask the user to confirm or provide edits before writing.

---

## ✏️ Step 2e — Create branch and write files

Once confirmed:

1. `git -C <REPO_PATH> checkout -b feature/add_<WORKLOAD_DIR>_<INSTANCE_SUFFIX>_vm_config`

2. **Scenario A:** Create the directory and write all four files:
   ```bash
   mkdir -p <REPO_PATH>/envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>
   ```
   Copy `secrets.tf`, `variables.tf`, `versions.tf` verbatim from the template directory.
   Write the generated instance file.

   **Scenario B:** Write only the generated instance file into the existing directory.

3. Verify: `git -C <REPO_PATH> diff --stat`

---

## 🚀 Step 2f — Commit, push, raise PR

```bash
git -C <REPO_PATH> add envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>/
git -C <REPO_PATH> commit -m "feat(<ENV>/<TIER>): add <WORKLOAD_DIR> <OS_TYPE> VM configuration"
git -C <REPO_PATH> push -u origin feature/add_<WORKLOAD_DIR>_<INSTANCE_SUFFIX>_vm_config
gh pr create \
  --repo pyrc-ghe-engineering/pyrc-iac-tf \
  --base main \
  --title "feat(<ENV>/<TIER>): add <WORKLOAD_DIR> <OS_TYPE> VM configuration" \
  --body "Adds Terraform configuration for \`<WORKLOAD_DIR>\` <OS_TYPE> VM (\`<APPLICATION_OWNER>\`) in \`<ENV>/<TIER>\`.

Scalr will automatically pick up the new config and run plan/apply after merge.

Please request review from the DevOps team."
```

Output the PR URL:

> "**Phase 2 complete.** PR raised: \<url\>
>
> Once the DevOps team reviews and merges this PR, Scalr will run \`terraform plan\` and
> \`terraform apply\` automatically."
