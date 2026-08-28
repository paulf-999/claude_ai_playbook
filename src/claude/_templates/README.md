# 📋 Templates Directory

Centralized templates for skills and other Claude configuration artifacts. This directory is synced to `~/.claude/_templates/` during `make update`.

## Directory Structure

```
_templates/
├── skills/                  # Skill-related templates
│   ├── SKILL.md.template
│   └── skill.contract.yaml.template
└── README.md                # This file
```

## Templates

### Skills

**`skills/SKILL.md.template`**
- Standard skill documentation template with 8 sections
- Maturity-gated design (draft → tactical → strategic)
- Used by: `/skill_creator` tool

**`skills/skill.contract.yaml.template`**
- Contract definition for skills (name, version, maturity, triggers, requirements)
- Enforces contract-first design pattern
- Used by: `/skill_creator` tool during initial setup

## Usage

When creating new skills, use `/skill_creator` command which will scaffold using these templates.

## Maintenance

- **Sync with global:** After updating templates here, run `make update` to sync to `~/.claude/_templates/`
- **Keep in sync:** The playbook repo is the source of truth. Updates to `~/.claude/_templates/` should be backported here.
