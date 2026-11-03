<!-- version: 1.2.0 -->
<!-- created: 2026-11-02 -->
<!-- updated: 2026-11-03 -->
# 👥 Writing style — Audience and depth

**Purpose:** Match technical depth and formality to the reader, open each page clearly, and write so a newcomer can follow it.

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

## 🚪 Openings

- 🎯 **Purpose first:** put `**Purpose:**` and one full sentence on what the page covers on the line after the H1.
- 🧭 **Navigation second:** after the Purpose line, say in a plain sentence which page this one belongs to, rather than opening with a bare `Part of` link.
- 📝 **Sentences over fragments:** write the opening as prose, not as stacked labels.

## 🧊 No assumed knowledge

- 🔤 **Define on first use:** explain every term the first time it appears, including ones this project coined, such as a named test or review.
- 🔗 **Descriptive links:** make the link text say what the linked page is, rather than describing it in a clause after the link.
- 📅 **No back-story:** don't rely on earlier PRs, plans or chats the reader hasn't seen.
- 🗣️ **Test:** read each sentence as someone who has never seen the repo, and rewrite any they couldn't follow.
