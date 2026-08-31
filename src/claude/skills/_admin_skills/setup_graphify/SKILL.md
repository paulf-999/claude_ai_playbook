---
name: claude_setup_graphify
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
    - /claude_setup_graphify
  contextual:
    - user wants to set up Graphify on a repo
    - user wants to reduce token usage for codebase exploration
not_for:
  - querying an existing graph — use /graphify for that
output:
  type: conversational
  confirmation_required: false
---

## 🎯 Purpose

Generates a local AST-based knowledge graph for a codebase, enabling structural queries without reading individual files.

## 📋 Overview

[Graphify](https://github.com/lucasrosati/claude-code-memory-setup) (`pip install graphifyy`) builds a local AST-based knowledge graph of a codebase. Once set up, the `/graphify` skill answers structural questions (what calls X, where is Y defined) from the graph.

## 🎯 Quality Scorecard

| Dimension | Score |
|---|---|
| **Design** | 8/10 |
| **Complexity** | 4/10 |
| **Test Coverage** | 6/10 |
| **Code Quality** | 7/10 |
| **Security** | 6/10 |
| **Documentation** | 8/10 |
| **Standards** | 8/10 |
| **Overall** | 7/10 |

## 🎯 Scope

**Draft maturity:** Happy path only; no error handling or refactoring.

## ✨ Capabilities

**Can do:** Generate AST-based knowledge graphs · Enable `/graphify` structural queries · Reduce token cost for codebase exploration

**Can't do:** Query existing graphs · Support unsupported languages · Index external codebases

## 🔒 Security

**Data handling:** Local AST graph in `graphify-out/` (generated, non-sensitive)  
**Access:** Reads repo files; writes to `graphify-out/` and `.gitignore`  
**Reversibility:** Fully reversible — delete output, remove entries, uninstall hook

## 📋 Prerequisites

- Bash, Read, Edit tools
- Python + pip (to install `graphifyy`)
- Local repository with code

## 🛠️ Workflow

See [_workflow_details.md](_workflow_details.md) for complete setup:
1. Install graphify CLI
2. Extract the knowledge graph
3. Add `graphify-out/` to `.gitignore`
4. Update repo `CLAUDE.md`

Ask structural questions in Claude to verify `/graphify` skill is working.

## 🚨 Error Recovery

| Issue | Fix |
|---|---|
| Package not found | `pip install graphifyy`; verify Python 3.8+ |
| Graph not created | Verify extraction command ran; check code files exist |
| `/graphify` not callable | Verify `graphify install --platform claude`; restart session |
| API errors | Check API key; verify quota; retry |

## 📌 Known Gaps

- **Git hook cost** — Not yet evaluated; pending decision
- **Language support** — Python/JS/TS best; others limited
