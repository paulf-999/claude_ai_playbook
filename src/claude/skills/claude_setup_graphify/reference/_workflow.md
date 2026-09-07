# Workflow & FAQ

## Five-Phase Setup

**Pre-flight validation:**
- Git repo: `git rev-parse --git-dir`
- Python 3.8+: `python3 --version | grep -E "3\.[89]|3\.1[0-9]"`
- Writable target: `touch graphify-out/.test && rm graphify-out/.test`

**Phase 1:** `pip install graphifyy && graphify install --platform claude`  
→ Verify: `python3 -c "import graphifyy"`

**Phase 2:** `graphify extract graphify-out/` (from repo root)  
→ Verify: `jq empty graphify-out/graph.json`  
Cost: ~$0.05–$0.10 first run (LLM-based), incremental after

**Phase 3:** `printf '\ngraphify-out/\n' >> .gitignore`  
→ Verify: `grep graphify-out/ .gitignore` (no duplicates)

**Phase 4:** Add Graphify section to CLAUDE.md with graph path  
→ Verify: `grep "## Graphify" CLAUDE.md`

**Phase 5:** Test `/graphify "List files"` from repo directory  
→ Verify: Skill responds within 10 seconds

**Safe operation pattern (all phases):**
1. Pre-check state before operation
2. Execute command
3. Verify with simple test
4. Report success or error with recovery step

**Utility flags** (see SKILL.md for details):
- `--dry-run` Preview without executing
- `--skip-extract` Reuse existing graph
- `--state` Check which phases completed

---

## FAQ

**Do I need to run this in every repository?**  
Yes, once per repo. Generates a repo-specific `graphify-out/graph.json`.

**How much does Graphify cost?**  
First extraction ~$0.05–$0.10 depending on codebase size. Subsequent runs are cheaper (incremental).

**How much does /graphify save vs. reading files?**  
Typical savings: 50–90%. Reading 100 files = 50K+ tokens. Querying graph = 500–5K tokens.

**Can I see which phases are done?**  
Yes: `/claude_setup_graphify --state` shows completion for all 5 phases.

**How do I update the graph after code changes?**  
Run Phase 3 only: `graphify extract graphify-out/`. Phases 1, 2, 4, 5 don't need to re-run.

**How do I undo the setup?**  
Delete `graphify-out/`, remove entry from `.gitignore`, remove Graphify section from `CLAUDE.md`.

**Can multiple developers run this simultaneously?**  
Yes. The skill is safe for concurrent runs. Duplicate detection prevents corruption.

**Troubleshooting Quick Links**
- **"not in git repo"** → `cd` to a git repository first
- **"Python 3.8+ required"** → Upgrade Python: `python3 --version` should be ≥3.8
- **"directory not writable"** → Check: `ls -ld graphify-out/`
- **"/graphify not callable"** → Restart Claude or reinstall: `graphify install --platform claude`
- **"extraction timed out"** → Repo too large. Try: `graphify extract --pattern "src/**"`

See `_troubleshooting.md` for full recovery details.
