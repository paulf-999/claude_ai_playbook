# Troubleshooting Guide

## Installation Issues

**"command not found: graphify"**
- Cause: graphify not in PATH after pip install
- Fix: Run `pip show graphifyy` to confirm installation. Try `graphify --help`. Restart shell session.

**"Permission denied: pip install"**
- Cause: pip requires sudo or virtual environment
- Fix: Use virtual environment: `python3 -m venv venv && source venv/bin/activate && pip install "graphifyy==0.8.36"`

**"No module named 'graphify'"**
- Cause: Python version mismatch or incorrect package name
- Fix: Verify `pip install "graphifyy==0.8.36"` — the package is `graphifyy` but the module you import is `graphify`. Confirm Python 3.8+: `python3 --version`

---

## Extraction Issues

**"No code files found in repo"**
- Cause: graphify cannot locate code files (empty repo, wrong directory, .gitignored files only)
- Fix: Verify repo has source files. Check `.gitignore` doesn't exclude all code. Run from correct repo root.

**"Extraction timed out"**
- Cause: Large repo (>10K files) or slow network
- Fix: Extract one subfolder first (`graphify extract src`), or raise the LLM timeout with `--api-timeout 1200`. Check network connectivity.

**"graph.json is invalid or empty"**
- Cause: Extraction failed silently or LLM API errors
- Fix: Check API key validity. Verify LLM quota. Re-run with an explicit backend, e.g. `graphify extract . --backend claude`, to see which key it uses

**"Extraction cost higher than expected"**
- Cause: Non-code files being analyzed (docs, configs, assets)
- Fix: Extract only the code folders (e.g. `graphify extract src`), or run with no LLM API key set so the semantic pass is skipped

---

## Configuration Issues

**".gitignore append failed"**
- Cause: File permission denied or disk full
- Fix: Check permissions: `ls -la .gitignore`. Verify disk space: `df -h`. Edit manually if script fails.

**"CLAUDE.md already has Graphify section"**
- Cause: Previous setup or manual edit
- Fix: Check CLAUDE.md for existing `## Graphify` section. Remove old section before re-running or manually merge.

**"Graphify section not appearing in CLAUDE.md"**
- Cause: File write succeeded but content not visible
- Fix: Verify edit with: `tail -20 CLAUDE.md`. Check file encoding (should be UTF-8).

---

## Verification Issues

**"/graphify skill not callable"**
- Cause: Skill installation failed or not in PATH
- Fix: Verify skill exists: `ls ~/.claude/skills/graphify/`. Restart Claude Code session. Check SKILL.md in ~/.claude/skills/.

**"/graphify returns no results"**
- Cause: graph.json not found or invalid format
- Fix: Verify file exists: `ls -la graphify-out/graph.json`. Check it's valid JSON: `jq empty graphify-out/graph.json`

**"/graphify slow or timing out"**
- Cause: Large graph or slow LLM API
- Fix: Check graph size: `wc -c graphify-out/graph.json`. Try simple query first: "What files are in this repo?"

---

## State Recovery

**"Setup interrupted mid-way (partial state)"**
- Cause: Script failure or user abort
- Fix: Check which phases completed. Manually complete remaining phases or re-run from phase 1 (safe to re-run — duplicate detection handles it).

**"Need to rollback setup"**
- Cause: Want to remove Graphify from repo
- Fix: Delete `graphify-out/` and remove entries from `.gitignore` and `CLAUDE.md`. Run `graphify uninstall --platform claude`.

**"Graph is stale (repo changed)"**
- Cause: Code changed after extraction
- Fix: Run `graphify update .`, which re-extracts code only, with no LLM. No need to re-run other phases.
