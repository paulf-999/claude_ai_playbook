---
name: claude_setup_graphify
description: Set up Graphify on a repo to generate a local AST-based knowledge graph, reducing token cost for codebase exploration
version: 0.1.0
maturity: draft
tags:
  criticality: could
  status: active
  tested: true
  test_coverage_level: comprehensive
---

## 🎯 Purpose

Set up [Graphify](https://github.com/lucasrosati/claude-code-memory-setup) on a repo to generate an AST-based knowledge graph:
- **Generate AST graph** — Five-phase setup (install → extract → gitignore → CLAUDE.md → verify)
- **Enable /graphify skill** — Structural queries without reading files
- **Reduce token costs** — Graph queries cost 2–5% of file reads
- **One-time setup** — Configure once per repo; reuse for all future sessions

## 💡 Example Usage

```
$ /claude_setup_graphify

Setting up Graphify on repo: ~/git_repos/core/dbt-analytics

1️⃣ Installing graphifyy package...
   ✅ graphifyy installed (v2.1.0)

2️⃣ Extracting knowledge graph...
   Target directory: graphify-out/
   ✅ graph.json created (127.4 KB)
   💰 Cost: ~$0.08 (first extraction; subsequent: ~$0.01)

3️⃣ Adding graphify-out/ to .gitignore...
   ✅ .gitignore updated

4️⃣ Updating CLAUDE.md...
   ✅ Graphify section added with /graphify instructions

5️⃣ Verifying setup...
   ✅ /graphify skill callable
   ✅ Test query: "What imports dbt_utils?"
   ✅ Response: Found in models/staging/stg_*.sql (10 matches)

Setup complete! Graph ready for queries.
```

## ✨ Best For

Creating knowledge graphs for large codebases where token cost for file reads is a constraint. Best for repos with 1,000+ files or deeply nested structures.

**Caveats:** One-time setup per repo. Language support limited to Python, JavaScript, and TypeScript (best AST coverage). Requires graphifyy v2.0+. Updates to repo require re-extraction (not incremental).

**Special Note — Response Standards Waiver:**
- This skill uses custom interactive output format (multi-phase setup workflow)
- Free-form prompts are incompatible with standard Claude response formatting requirements
- The response standards rule makes an exception for this skill to preserve interactive capability

## 📚 References

**Setup & Workflow:**
- `reference/_workflow.md` — Five-phase setup procedure and recovery steps
- `evals.yaml` — Six test scenarios covering all phases

**Quality:**
- `reference/_quality_scorecard.md` — Quality assessment and Draft maturity justification

