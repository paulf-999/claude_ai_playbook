# 🏷️ Payroc Engineering Naming Standards (Index)

**Purpose:** Company-wide naming standards for all Payroc engineering resources — repositories, infrastructure, and automation jobs.

**Source of truth:** [DM - Payroc Naming Standards (Reference)](https://payroc.atlassian.net/wiki/spaces/DA/pages/5112365057) in Confluence.

---

## 📋 Child Pages

Choose the guide for your task:

| Guide | Purpose | When to use |
|-------|---------|------------|
| **[_naming_conventions.md](payroc_engineering_naming_standards/_naming_conventions.md)** | Core naming rules and segment definitions | Creating any named resource; understanding naming standards |
| **[_naming_repositories.md](payroc_engineering_naming_standards/_naming_repositories.md)** | Repository naming patterns and examples | Creating or naming a Git repository |
| **[_naming_infrastructure.md](payroc_engineering_naming_standards/_naming_infrastructure.md)** | VM hostnames, cloud resources, PCI scope codes, asset roles | Provisioning VMs or cloud infrastructure |

---

## 🎯 Quick Reference

**Repository pattern:** `[dept]-[type]-[descriptor]`
- Example: `dmt-scripts-claude_ai_playbook`

**VM hostname pattern:** `[environment]-[site]-[asset-role]-[#].payroc.io`
- Example: `prd-us-app-01.payroc.io`

**Cloud resource pattern:** `[dept]-[env]-[site]-[type]-[descriptor]`
- Example: `dmt-prd-us-s3-dbt-models`

---

## ✅ Before Creating a Named Resource

1. Check `_naming_conventions.md` for valid segment codes
2. Choose the appropriate guide based on resource type
3. Follow the pattern and verify against examples
4. Validate using the checklist in the relevant guide
