---
name: setup_graphify
description: Set up Graphify on a repo to generate a local AST-based knowledge graph, reducing token cost for codebase exploration.
version: 0.1.0
maturity: draft
tags:
  criticality: could
  status: active
  tested: true
tools: Bash, Read, Edit
triggers:
  explicit:
    - /setup_graphify
  contextual:
    - user wants to set up Graphify on a repo
    - user wants to reduce token usage for codebase exploration
not_for:
  - querying an existing graph — use /graphify for that
output:
  type: conversational
  confirmation_required: false
---

## 🔬 Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## 📋 Overview

[Graphify](https://github.com/lucasrosati/claude-code-memory-setup) (`pip install graphifyy`) builds a local AST-based knowledge graph of a codebase. Once set up, the `/graphify` skill can answer structural questions (what calls X, where is Y defined, trace Z) from the graph rather than reading individual files.

**First-time setup for a repo — run these steps once:**

---

## 🚀 Phase 1 — Install

```bash
pip install graphifyy
graphify install --platform claude
```

`graphify install --platform claude` installs the `/graphify` query skill into `~/.claude/skills/`.

The `/graphify` trigger block is persisted in `src/claude/process/graphify.md` and loaded via `@import` in `src/claude/CLAUDE.md` — it survives playbook syncs.

---

## 📊 Phase 2 — Extract the knowledge graph

See [phase2.md](phase2.md) — extract commands, repo-specific example, known output path issue, and API cost note.

---

## 🗑️ Phase 3 — Add to .gitignore

The `graphify-out/` directory is generated output — do not commit it:

```bash
# Add to .gitignore at repo root
printf '\n# Graphify — generated knowledge graph output (do not commit)\ngraphify-out/\n' >> .gitignore
```

---

## 📝 Phase 4 — Update the repo CLAUDE.md

Add or confirm the Graphify section in the repo's `CLAUDE.md` points to the correct graph path. See the Graphify section in `da-etl-dbtanalytics/CLAUDE.md` as a reference template.

---

## 🪝 Phase 5 — Git hook (optional)

Auto-rebuilds the graph on every commit (incremental, only changed files):

```bash
cd <repo-root>
graphify hook install
```

> ⚠️ The hook triggers semantic extraction on changed non-code files, which has a small OpenAI/Gemini cost per commit. Evaluate whether this overhead is acceptable before installing. Not yet set up on `da-etl-dbtanalytics`.
>
> TODO (tactical): evaluate hook cost on a typical commit cadence and decide whether to enable.

---

## ✅ Verification

After setup, confirm the skill is working:
1. Open a Claude session in the repo directory
2. Ask a structural question — e.g. "What models ref dim_merchant?"
3. The `/graphify` skill should answer from the graph without reading files

---

## 📌 Repos where Graphify is set up

See [repos.md](repos.md) — running list of repos with graph paths, setup dates, and known issues.
