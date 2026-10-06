# 📋 Templates Directory

Centralized templates for skills and other Claude configuration artifacts. This directory is copied to `~/.claude/_templates/` by `make install`.

## Directory Structure

```
_templates/
├── skills/                  # Skill-related templates
│   ├── SKILL.md.template
│   ├── skill.contract.yaml.template
│   └── _quality_scorecard_template.md
├── AGENT.md.template        # Starting point for a new agent
├── rule.md.template         # Starting point for a new rule
├── TODO.md.template         # Starting point for a project TODO list
├── scorecard.md.template  # Layout for every individual scorecard
├── scorecard_summary.md.template  # Layout for every scorecard summary
├── template_bash_script.sh  # Starting point for a new bash script
├── utils/
│   └── shell_utils.sh       # Shared shell helpers: log colours and common variables
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

### Agents, rules and TODOs

**`AGENT.md.template`**
- Starting point for a new agent at `agents/<group>/<name>/AGENT.md`: frontmatter, metadata header and the standard sections
- Keeps its uppercase name because it mirrors the `AGENT.md` file it produces
- Used by: `_rules_lazy_load/authoring_guidelines/authoring_agents/_core_standards.md`

**`rule.md.template`**
- Two starting points for a new rule: Template A (one principle) and Template B (several related patterns)
- Ends with a quality checklist that applies to both templates
- Used by: `authoring_rules.md`

**`TODO.md.template`**
- Table layout for a project's `TODO.md`, with pending and completed items
- Keeps its uppercase name because it mirrors the `TODO.md` file it produces

### Scripts

**`template_bash_script.sh`**
- Starting point for a new bash script: shebang, safety flags, `shell_utils.sh` source, section headers, trap and logging
- Used by: `rules/04_path_scoped/style_guide_standards/bash.md`

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

- **Sync with global:** After updating templates here, run `make install` to copy them to `~/.claude/_templates/`
- **Keep in sync:** The playbook repo is the source of truth. Updates to `~/.claude/_templates/` should be backported here.
