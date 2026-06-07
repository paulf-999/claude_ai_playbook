# 🏗️ Phase 1 — Workspace PR

**Goal:** Register the new VM directory as a Scalr workspace by adding an entry to `workspaces.tfvars`.

---

## 📋 Step 1a — Read and show the proposed change

Read `<REPO_PATH>/envs/<ENV>/apps/workspaces.tfvars`.

Check whether an entry for `<TIER>/<WORKLOAD_DIR>` already exists. If it does, report it and ask
whether to proceed (the workspace may already be registered from a previous attempt).

Show the proposed new entry:

```
{ name = "<TIER>/<WORKLOAD_DIR>", pci_scope = "<PCI_SCOPE>", excluded_sites = ["am1"] },
```

Show a before/after diff snippet indicating where it will be inserted. Ask the user to confirm
before writing anything.

---

## ✏️ Step 1b — Create branch and edit the file

Once confirmed:

1. `git -C <REPO_PATH> checkout -b feature/add_<WORKLOAD_DIR>_workspace`

2. Insert the entry into `workspaces.tfvars`. Insertion rules:
   - Insert in alphabetical order within the tier block (e.g. among other `dte/` entries).
   - If no entries for this tier exist yet, append after the last entry in the list.
   - Preserve the exact indentation and spacing style of adjacent entries.
   - Ensure there is no trailing comma after the final entry in the list.

3. Verify the edit: `git -C <REPO_PATH> diff`

---

## 🚀 Step 1c — Commit, push, raise PR

```bash
git -C <REPO_PATH> add envs/<ENV>/apps/workspaces.tfvars
git -C <REPO_PATH> commit -m "feat(scalr): add <TIER>/<WORKLOAD_DIR> workspace entry"
git -C <REPO_PATH> push -u origin feature/add_<WORKLOAD_DIR>_workspace
gh pr create \
  --repo pyrc-ghe-engineering/pyrc-iac-tf \
  --base main \
  --title "feat(scalr): add <TIER>/<WORKLOAD_DIR> workspace entry" \
  --body "Adds Scalr workspace for \`<TIER>/<WORKLOAD_DIR>\` in \`<ENV>\`.

Once merged, Scalr will register the directory and allow the VM configuration PR to run plan/apply.

Please request review from the DevOps team."
```

---

## ⏸️ Step 1d — Pause for merge

Output the PR URL and stop:

> "**Phase 1 complete.** PR raised: \<url\>
>
> Wait for the DevOps team to review and merge this PR before continuing. Once merged,
> resume with \`/provision_vm phase2\` to raise the VM configuration PR.
>
> **Note your parameters** — you will need to re-enter them when invoking phase2:
> \`ENV\`, \`TIER\`, \`WORKLOAD_DIR\`, \`APPLICATION_OWNER\`, \`ASSET_ROLE\`, \`INSTANCE_SUFFIX\`,
> \`COMPUTE_RESOURCES\`, \`DISKS\`, \`PATCH_GROUP\`."
