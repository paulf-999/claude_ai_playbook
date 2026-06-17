# Phase 2 — Extract the knowledge graph

## 📊 Phase 2 — Extract the knowledge graph

Run from the **project root** (not a subdirectory) to avoid double-nested output paths:

```bash
cd <repo-root>
graphify extract <target-dir>
```

For `da-etl-dbtanalytics`:
```bash
cd ~/git_repos/core/da-etl-dbtanalytics
graphify extract prod_analytics/
```

Output lands at `graphify-out/graph.json` relative to where you ran the command.

> ⚠️ **Known issue (first run on this repo):** Graphify was initially run as `graphify extract . --out ./graphify-out` from inside `prod_analytics/`, causing double-nested output at `prod_analytics/graphify-out/graphify-out/graph.json`. Future runs should follow the pattern above.
>
> TODO (tactical): re-run from repo root to produce a clean `graphify-out/graph.json` at `da-etl-dbtanalytics/graphify-out/graph.json` and update CLAUDE.md accordingly.

**Cost note:** Graphify uses semantic extraction (LLM) for non-code files (docs, YAMLs). If no `GEMINI_API_KEY` is set, the CLI falls back to OpenAI. First run on `prod_analytics/` cost ~$0.07 (151k tokens in, 5.5k out). Subsequent runs are incremental — only changed files are re-processed. Set `GEMINI_API_KEY` to use Gemini instead.
