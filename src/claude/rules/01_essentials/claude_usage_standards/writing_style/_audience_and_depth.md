<!-- version: 1.0.0 -->
<!-- created: 2026-11-02 -->
<!-- updated: 2026-11-02 -->
# 👥 Writing style — Audience and depth

**Purpose:** Match technical depth and formality to the reader, and give long content its whole idea up front.

---

## ✍️ Before writing

- 🎯 **Confirm the audience:** before writing for people outside the repo (Confluence, Jira, email, comms), confirm who it's for and set the depth from the table below.
- ❓ **Ask when unsure:** if the audience is unknown or spans several groups, ask before writing.

| Audience | Content focus | Technical level | Emojis | Depth |
|---|---|---|---|---|
| 💼 **Management** | Business outcomes | None | None | • **Plain:** no jargon or domain terms.<br>• **Project-level:** progress, status, decisions and risks. |
| 🔭 **Technical management** | Strategy and outcomes | Partial | Headings only | • **Strategy-level:** outcomes and concepts, aware of the technology.<br>• **Not mechanics:** leave out implementation detail. |
| 📊 **Data analytics team** | Data and insights | Partial | Headings only | • **Semi-technical:** knows data concepts and the business domain.<br>• **Meaning first:** what the data means, not how it's produced. |
| 🗄️ **Data engineering team** | Technical implementation | Full | Headings only | • **Fully technical:** data stack focus, such as Airflow, dbt, Snowflake and connectors. |
| ⚙️ **Infrastructure / DevOps** | Infra and operations | Full | Headings only | • **Fully technical:** infra focus, such as VMs, networking, Ansible, OS and cloud. |

## 📋 Executive Summary

- 📋 **When:** open long-form content (blog posts, Confluence pages, reports and repo parent pages) with a `📋 Executive Summary`.
- 🔢 **Shape:** 3–5 bullets that give the whole idea before any detail.
- 🪜 **Why:** it's the first layer of progressive disclosure, and the written counterpart of the chat Summary in `claude_response_standards.md`.
