---
name: claude_setup_graphify
description: Set up Graphify on a repo to generate a local AST-based knowledge graph, reducing token cost for codebase exploration
maturity: strategic
tags:
  criticality: could
  status: active
  tested: true
  test_coverage_level: comprehensive
---
<!-- version: 2.1.0 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-10-29 -->

## 🤖 Instructions for Claude

- **Pre-check:** run every pre-flight check in `reference/_implementation.md` (git repo, repo root, not root, no symlinked targets, Python 3.8+, writable root), and stop and report any failure.
- **Read first:** read `reference/_implementation.md` for the five phases, and `reference/_security.md` before Phase 1.
- **Always:** install with `pip install "graphifyy==0.8.36"`, never an unpinned `pip install graphifyy`.
- **Always:** before Phase 2, tell the user that code stays local but docs, PDFs and images get an LLM pass when an API key is set, and wait for a yes.
  - **On a no:** stop without extracting anything.
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

Large codebases, around 1,000 files or more, where reading files costs too many tokens. Currently at the **strategic** stage — setup, pre-flight and security checks, the data-sharing prompt, re-runs and error recovery are covered, with scope fixed to the five phases.

**Caveats:** one-time setup per repo, and the graph must be re-extracted after code changes. Pinned to graphifyy 0.8.36. The contract sets `waives_response_standards: true`, so the setup keeps its own step-by-step format.

## ⚠️ Known gaps

- **Stale graph:** nothing re-extracts the graph after code changes, so answers drift from the code over time.
  - **Workaround:** run `graphify update .` from the repo root after significant changes.
- **One pinned version:** the skill is tested only against graphifyy 0.8.36.
  - **Workaround:** stay on the pin, and re-run the evals by hand before raising it.
- **Unrun scenarios:** nothing runs `tests/evals.yaml` yet, which #463 tracks.
  - **Workaround:** check a change against the scenarios by hand before merging it.

## 📚 References

- `reference/_implementation.md` — the five phases, flags (`--dry-run`, `--skip-extract`, `--state`) and FAQ
- `reference/_security.md` — what leaves the machine, the version pin and file safeguards
- `reference/_troubleshooting.md` — common install and extraction errors
- `reference/_examples.md` — example setup scenarios
- `tests/evals.yaml` — 17 test scenarios covering checks, phases, errors, five adversarial and security cases, and a not_for case
- `_reference/_quality_scorecards/skills/scorecard_claude_setup_graphify.md` — quality scorecard
