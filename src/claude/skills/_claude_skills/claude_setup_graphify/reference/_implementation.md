# Workflow & FAQ

## Five-Phase Setup

**Pre-flight validation (stop and report on any failure, before installing anything):**
- Git repo: `git rev-parse --git-dir`
- Repo root: `cd "$(git rev-parse --show-toplevel)"`, and refuse any target path that resolves outside it, such as `../`
- Not root: `[ "$(id -u)" -ne 0 ]`
- No symlinks: `[ ! -L .gitignore ] && [ ! -L CLAUDE.md ] && [ ! -L graphify-out ]`, so no write follows a link out of the repo
- Python 3.8+: `python3 --version | grep -E "3\.[89]|3\.1[0-9]"`
- Writable target: `[ -w . ]` on the repo root, which works before `graphify-out/` exists

**Phase 1:** `pip install "graphifyy==0.8.36" && graphify install --platform claude`
→ Verify: `python3 -c "import graphify"` (the package is `graphifyy`, the module is `graphify`)
→ Pinned: 0.8.36 is the version in use; bump it deliberately after checking the release notes

**Phase 2:** `graphify extract .` (from repo root — the argument is the folder to read, and the graph is written to `./graphify-out/`)
→ Verify: `jq empty graphify-out/graph.json`
→ Confirm first: tell the user what leaves the machine (see `_security.md` → Data leaving the machine) and get a yes before extracting a work repo
→ On a no: stop without extracting, skip Phases 3–5, and report that nothing left the machine
Cost: code parsing is local and free; only a semantic pass over docs, PDFs or images uses an LLM, billed to the API key it runs with

**Phase 3:** `grep -qx 'graphify-out/' .gitignore || printf '\ngraphify-out/\n' >> .gitignore`
→ Verify: `grep -cx 'graphify-out/' .gitignore` returns 1, so a re-run adds no duplicate

**Phase 4:** Add a Graphify section to CLAUDE.md with the graph path, only if `grep -q "## Graphify" CLAUDE.md` finds none
→ Verify: `grep -c "## Graphify" CLAUDE.md` returns 1

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
Parsing code is free, because it runs locally with tree-sitter. Only the semantic pass over docs, PDFs and images uses an LLM, billed to whichever API key is set.

**How much does /graphify save vs. reading files?**
Typical savings: 50–90%. Reading 100 files = 50K+ tokens. Querying graph = 500–5K tokens.

**Can I see which phases are done?**
Yes: `/claude_setup_graphify --state` shows completion for all 5 phases.

**How do I update the graph after code changes?**
Run `graphify update .` from the repo root. It re-extracts code only, with no LLM, and no other phase needs to re-run.

**How do I undo the setup?**
Delete `graphify-out/`, remove entry from `.gitignore`, remove Graphify section from `CLAUDE.md`.

**Can multiple developers run this simultaneously?**
Yes. The skill is safe for concurrent runs. Duplicate detection prevents corruption.

**Troubleshooting Quick Links**
- **"not in git repo"** → `cd` to a git repository first
- **"Python 3.8+ required"** → Upgrade Python: `python3 --version` should be ≥3.8
- **"directory not writable"** → Check: `ls -ld graphify-out/`
- **"/graphify not callable"** → Restart Claude or reinstall: `graphify install --platform claude`
- **"extraction timed out"** → Repo too large. Extract one subfolder first (`graphify extract src`), or raise `--api-timeout`

See `_troubleshooting.md` for full recovery details.
