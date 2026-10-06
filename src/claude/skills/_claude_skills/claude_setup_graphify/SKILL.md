---
name: claude_setup_graphify
description: Set up Graphify on a repo to generate a local AST-based knowledge graph, reducing token cost for codebase exploration
maturity: tactical
tags:
  criticality: could
  status: active
  tested: true
  test_coverage_level: comprehensive
---
<!-- version: 1.2.1 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-10-06 -->

## 🤖 Instructions for Claude

- **Pre-check:** confirm the folder is a git repo, Python is 3.8 or newer and the repo root is writable, and stop and report any failure.
- **Read first:** read `reference/_workflow.md` for the five phases, and `reference/_security.md` before Phase 1.
- **Always:** install with `pip install "graphifyy==0.8.36"`, never an unpinned `pip install graphifyy`.
- **Always:** before Phase 2, tell the user that code stays local but docs, PDFs and images get an LLM pass when an API key is set, and wait for a yes.
- **Never:** run as root, write outside `$(git rev-parse --show-toplevel)`, or commit `graphify-out/`.

## 🎯 Purpose

Sets up [Graphify](https://github.com/Graphify-Labs/graphify) on a repo so Claude can query a knowledge graph instead of reading files:
- **Build the graph** — five phases: install, extract, gitignore, CLAUDE.md, verify.
- **Enable /graphify** — structural questions answered from `graphify-out/graph.json`.
- **Cut token cost** — a graph query costs a small fraction of reading the files.
- **One-time setup** — once per repo, reused in every later session.

## 💡 Example Usage

```
$ /claude_setup_graphify

Setting up Graphify on repo: ~/git_repos/core/dbt-analytics
1️⃣ Installing... ✅ graphifyy 0.8.36 installed (pinned)
2️⃣ Code is parsed locally. Docs get an LLM pass only if an API key is set — continue? y
   ✅ graph.json created (127.4 KB)
3️⃣ ✅ graphify-out/ added to .gitignore
4️⃣ ✅ Graphify section added to CLAUDE.md
5️⃣ ✅ /graphify answered a test query

Setup complete! Graph ready for queries.
```

## ✨ Best For

Large codebases, around 1,000 files or more, where reading files costs too many tokens. Currently at the **tactical** stage — setup, pre-flight checks and error recovery are covered, but scope may still change.

**Caveats:** one-time setup per repo, and the graph must be re-extracted after code changes. Pinned to graphifyy 0.8.36. The contract sets `waives_response_standards: true`, so the setup keeps its own step-by-step format.

## 📚 References

- `reference/_workflow.md` — the five phases, flags (`--dry-run`, `--skip-extract`, `--state`) and FAQ
- `reference/_security.md` — what leaves the machine, the version pin and file safeguards
- `reference/_troubleshooting.md` — common install and extraction errors
- `reference/_examples.md` — example setup scenarios
- `tests/evals.yaml` — 15 test scenarios covering checks, phases and errors
- `_admin/_quality_scorecards/skills/scorecard_claude_setup_graphify.md` — quality scorecard
