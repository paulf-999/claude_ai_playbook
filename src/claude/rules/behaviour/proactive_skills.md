# 🎯 Rules — Proactive skill dispatch

When a user request matches the contextual trigger of an installed skill, invoke the skill
rather than answering inline. Skill output is more structured and consistent than ad hoc prose.

## ⚙️ Admin

| If the user... | Invoke |
|---|---|
| Wants to clean up or archive old `~/.claude_<timestamp>` snapshot directories | `/archive_claude_config_snapshots` |
| Wants to sync or update the Claude playbook config | `/sync_playbook` |
| Wants to audit agents for quality or gaps | `/audit_agents` |
| Wants to audit installed skills for standards compliance | `/audit_skills` |
| Wants to set up Graphify on a repo | `/setup_graphify` |

## 🔍 Analysis

| If the user... | Invoke |
|---|---|
| Wants to stress-test a plan, find what could kill it, or work backwards from failure | `/premortem` |
| Wants adversarial critique, to find weaknesses, or to tear an idea apart | `/redteam` |
| Wants to surface implementation traps, hidden risks, or what they might be missing | `/pitfalls` |
| Is choosing between two or more options, tools, or approaches | `/compare` |
| Wants to question inherited assumptions or rebuild reasoning from scratch | `/first_principles` |
| Faces a complex or ambiguous problem and needs a structured path from information to action | `/ooda` |

## 🔗 Atlassian *(requires Atlassian MCP)*

| If the user... | Invoke |
|---|---|
| Wants to create a Confluence page | `/confluence_create_page` |
| Wants to review or critique a Confluence page | `/confluence_review_page` |
| Wants to create one or more Jira tickets | `/jira_create` |
| Wants to create sub-tasks under a Jira ticket | `/jira_subtask` |
| Wants to bulk-update fields across Jira tickets | `/jira_update` |
| Wants to check Jira tickets for missing or incorrect fields | `/jira_hygiene` |
| Wants to populate or score Business Value fields on Jira tickets | `/populate_jira_business_value` |

## 💬 Communication

| If the user... | Invoke |
|---|---|
| Needs a short stakeholder-ready summary for Slack, email, or Confluence | `/exec_summary` |
| Needs to explain a technical concept to a non-technical audience | `/eli5` |
| Wants to draft or review a Teams message or email | `/draft_comms` |

## 🛠️ Dev

| If the user... | Invoke |
|---|---|
| Wants to stress-test a plan or design via structured interview before implementation | `/grill_me` |

## 🌿 Git

> `/git_create_pr` is mandated by `rules/workflows.md` — do not wait for a contextual trigger; invoke it whenever a PR is to be raised.

| If the user... | Invoke |
|---|---|
| Wants to post a review comment on a GitHub PR | `/git_review_pr` |
| Wants to formally request changes on a PR with inline comments | `/git_request_changes_pr` |
| Wants to notify the team on Teams after raising a PR | `/git_notify_pr` |

## 🏗️ Infrastructure

| If the user... | Invoke |
|---|---|
| Wants to create a new Ansible role or playbook | `/ansible_playbook_creation` |
| Wants to provision a new VM via Terraform | `/provision_vm` |

## 📅 Meetings

| If the user... | Invoke |
|---|---|
| Is preparing for a 1-to-1 or weekly manager catch-up | `/weekly_one_to_one_prep` |
| Is doing sprint planning for the DPE team | `/sprint_planning_dpe_team` |
| Wants to schedule a meeting or draft a meeting invite | `/schedule_meeting` |

## ⚠️ When not to dispatch

- The user has already invoked the skill explicitly — do not re-invoke it.
- The request is a narrow, one-sentence question — a skill invocation would be overkill.
- The context is mid-task (e.g. "what could go wrong with this SQL join?") — answer inline;
  reserve dispatch for whole-plan or whole-proposal analysis.
- Atlassian skills require the Atlassian MCP to be active — check before dispatching.
