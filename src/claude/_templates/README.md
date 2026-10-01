# 📋 Templates Directory

Centralized templates for skills and other Claude configuration artifacts. This directory is synced to `~/.claude/_templates/` during `make update`.

## Directory Structure

```
_templates/
├── skills/                  # Skill-related templates
│   ├── SKILL.md.template
│   ├── skill.contract.yaml.template
│   └── _quality_scorecard_template.md
├── scorecard.md.template  # Layout for every individual scorecard
├── scorecard_summary.md.template  # Layout for every scorecard summary
└── README.md                # This file
```

## Templates

### Skills

**`skills/SKILL.md.template`**
- Standard skill documentation template: frontmatter, metadata header and 4 sections (Purpose, Example Usage, Best For, References)
- Maturity stage is stated in the Best For line (draft → tactical → strategic)
- Used by: `/skill_creator` tool

**`skills/skill.contract.yaml.template`**
- Contract definition for skills (name, version, maturity, triggers, requirements)
- Enforces contract-first design pattern
- Used by: `/skill_creator` tool during initial setup

**`skills/_quality_scorecard_template.md`**
- Table-only layout for each skill's scorecard at `_admin/_quality_scorecards/skills/scorecard_<skill_name>.md`: 7 dimensions plus Overall
- Includes the scoring scale and per-dimension criteria

### Scorecards

**`scorecard.md.template`**
- Shared layout for every individual scorecard: header dates, Overall score, Recommended improvements, dimension table and Related files
- Each type's dimensions and criteria live in its own template or README, which this file points to

**`scorecard_summary.md.template`**
- Shared layout for all six scorecard summaries in `_admin/_quality_scorecards/`: the top-level `quality_scorecards_summary.md` and each `<type>_scorecards_summary.md`
- Sections: Scores by group, Recommended next actions, All scorecards (All summaries in the top-level file) and Keeping this current

## Usage

When creating new skills, use `/skill_creator` command which will scaffold using these templates.

## Maintenance

- **Sync with global:** After updating templates here, run `make update` to sync to `~/.claude/_templates/`
- **Keep in sync:** The playbook repo is the source of truth. Updates to `~/.claude/_templates/` should be backported here.
