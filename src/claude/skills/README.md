# Skills

Reusable multi-step workflows invoked via `/skill-name` in Claude Code.

---

## 📄 Confluence

| Skill | What it does |
|---|---|
| `/create_confluence_page` | Interactive dispatcher — select a page pattern, gather inputs, and create a draft Confluence page. Patterns listed below. |

### Available patterns

| Pattern | Agent | What it does |
|---|---|---|
| `general_page` | Technical writer | Gathers title, purpose, and free-form sections → creates a general DM page using the standard template |
| `how_to` | Technical writer | Gathers prerequisites, steps (list or structured table), and notes → creates the how-to guide |
| `requirements` | Project manager | Elicits requirements with MoSCoW, user stories, and acceptance criteria → surfaces assumptions and out-of-scope items → creates the requirements page |
| `incident_report` | Technical writer | Gathers incident metadata, timeline, cause, resolution, actions, and next steps → creates the incident report page |
| `claude_component` | Technical writer | Documents a Claude Code component (hook, skill, agent, command, MCP server) for team knowledge sharing → creates the component page |

### Data Platform-specific patterns

| Pattern | Agent | What it does |
|---|---|---|
| `design_decision` | Architect | Gathers decision context and options → evaluates tradeoffs → creates the design decision page |
| `data_platform_sprint_goals` | Technical writer | Gathers Must / Should / Blocked items for a sprint → confirms content → creates the sprint goals page |
| `platform_risk_assessment` | Data platform architect | Walks through each maturity theme → rates and summarises → creates the risk & maturity assessment page |
| `initiative_idea` | Data platform architect | Gathers idea, trigger, and stack-fit sense-check → creates the lightweight initiative idea page |

---

## 💬 Communications

| Skill | What it does |
|---|---|
| `/draft_comms` | Dispatcher — select email or Teams, then follow the channel-specific pattern for drafting or reviewing a message |
| `/schedule_meeting` | Schedule a meeting — check calendar availability, propose a timeslot, draft the meeting invite body, and optionally draft a Teams follow-up message |
| `/catchup-prep` | Prepare for a 1-to-1 or weekly catch-up with a manager — gather topics, identify the core message, filter async vs. meeting items, prioritise, time-box, and produce a final agenda |

---

## 🛠️ Development

| Skill | What it does |
|---|---|
| `/commit` | Stage files and create a conventional commit — review diff, draft message, confirm, and commit |
| `/create_mr` | Full MR workflow: create branch, stage, commit, push, and open a GitHub PR following team conventions |
| `/release` | Create a GitHub Release for a completed phase — checks all phase issues are closed, generates a changelog from merged PRs, and publishes via `gh release create` |

---

## 🔧 Maintenance

| Skill | What it does |
|---|---|
| `/snapshot-archiving` | Archive `~/.claude_<timestamp>` snapshot directories into a two-tier age-based structure (`~/.claude_archived/` after 30 days, `~/.claude_deep_archived/` after 90 days) |

---

## 🧠 Productivity

| Skill | What it does |
|---|---|
| `/ideas` | Capture and browse ideas using the MCP memory server — log a title, description, category, and priority; retrieve existing ideas across sessions |
| `/todos` | Lightweight todo tracker — add, list, and close actionable work items backed by the MCP memory server |
