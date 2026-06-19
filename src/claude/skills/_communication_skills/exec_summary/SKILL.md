---
name: exec_summary
description: Generate a compact stakeholder-ready summary — context, what changed, business impact, and recommended action — for pasting into Slack, email, or Confluence.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
triggers:
  explicit:
    - /exec_summary
    - "exec summary"
    - "executive summary"
    - "summarise for stakeholders"
    - "write me a summary"
  contextual:
    - user needs to communicate a decision, incident, or update to a non-technical audience
    - user wants a paste-ready summary for Slack, email, or Confluence
not_for:
  - full technical write-ups or design docs — use /confluence_create_page
  - drafting a Teams or email message directly — use /draft_comms
output:
  type: conversational
  confirmation_required: false
tools: []
---

## 📊 Scope gate

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## 📄 Exec Summary

Produce a compact, stakeholder-ready summary. No jargon. No preamble. Written so a non-technical reader understands the situation and knows what is being asked of them.

### Step 1 — Extract the substance
From context, identify:
- What happened or what was decided
- Why it matters to the business
- What action (if any) is required from the reader

If the input is technical (e.g. an incident, a PR, a pipeline failure), translate it — no internal tool names, no implementation detail.

### Step 2 — Apply the enforced structure

Every exec summary has exactly four lines/blocks:

1. **Context** — one sentence: what this is about and why it exists
2. **What changed / happened** — one to two sentences: the specific event, decision, or update
3. **So what** — one sentence: the business impact (what this means for operations, customers, or risk)
4. **Action required** — one sentence or "No action required": what the reader needs to do and by when

### Step 3 — Validate

Before outputting, check:
- No internal tool names (Airflow, dbt, Snowflake, etc.) — describe by function if needed
- No sentences longer than 25 words
- No technical jargon unexplained by context
- Total length under 100 words

---

## 📋 Output format

**Context:** [one sentence]

**What happened:** [one to two sentences]

**So what:** [one sentence — business impact]

**Action required:** [one sentence, or "No action required"]
