# Skills

Reusable multi-step workflows invoked via `/skill-name` in Claude Code.

---

## Confluence

| Skill | What it does |
|---|---|
| `/create_confluence_page` | Interactive dispatcher — select a page pattern, gather inputs, and create a draft Confluence page in the `DA` space. Patterns listed below. |

### Patterns

| Pattern | Agent | What it does |
|---|---|---|
| `data_platform_sprint_goals` | Technical writer | Gathers Must / Should / Blocked items for a sprint → confirms content → creates the sprint goals page |
| `design_decision` | Data platform architect | Gathers decision context and options → evaluates tradeoffs → creates the design decision page |
| `initiative_idea` | Data platform architect | Gathers idea, trigger, and stack-fit sense-check → creates the lightweight initiative idea page |
| `platform_risk_assessment` | Data platform architect | Walks through each maturity theme → rates and summarises → creates the risk & maturity assessment page |
| `requirements` | Project manager | Elicits requirements with MoSCoW, user stories, and acceptance criteria → surfaces assumptions and out-of-scope items → creates the requirements page |
| `incident_report` | Technical writer | Gathers incident metadata, timeline, cause, resolution, actions, and next steps → creates the incident report page |
| `how_to` | Technical writer | Gathers prerequisites, steps (list or structured table), and notes → creates the how-to guide |
| `general_page` | Technical writer | Gathers title, purpose, and free-form sections → creates a general DM page using the standard template |

---

## Presentations

| Skill | Agent | What it does |
|---|---|---|
| `/create_pptx` | Technical writer | Gathers deck purpose, audience, and key messages → proposes slide structure → generates a `.pptx` file via python-pptx |

---

## Communications

| Skill | What it does |
|---|---|
| `/draft_comms` | Dispatcher — select email or Teams, then follow the channel-specific pattern for drafting or reviewing a message |
| `/schedule_meeting` | Schedule a meeting — check calendar availability, propose a timeslot, draft the meeting invite body, and optionally draft a Teams follow-up message |

---

## Development

| Skill | What it does |
|---|---|
| `/commit` | Stage files and create a conventional commit — review diff, draft message, confirm, and commit |
| `/create-mr` | Full MR workflow: create branch, stage, commit, push, and open a GitHub PR following team conventions |

---

## Directory structure

```
skills/
  create_confluence_page/
    SKILL.md
    patterns/
      data_platform_sprint_goals.md
      design_decision.md
      initiative_idea.md
      platform_risk_assessment.md
      requirements.md
      incident_report.md
      how_to.md
      general_page.md
    templates/
      data_platform_sprint_goals.md
      design_decision.md
      initiative_idea.md
      platform_risk_assessment.md
      requirements.md
      incident_report.md
      how_to.md
      general_page.md
  create_pptx/
    SKILL.md
  draft_comms/
    SKILL.md
    patterns/
      email.md
      teams.md
  schedule_meeting/
    SKILL.md
  commit/
    SKILL.md
  create-mr/
    SKILL.md
```
