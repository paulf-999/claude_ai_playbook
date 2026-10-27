# Quality Scorecard — claude_setup_graphify

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-27

**Overall score:** 6.3/10

**Recommended improvements:**
- Remove the `git add ... graphify-out/graph.json` step from `reference/_examples.md`, which contradicts SKILL.md's "Never commit `graphify-out/`"
- Define `--dry-run`, `--skip-extract` and `--state`, or delete them from `_workflow.md`, which says "see SKILL.md for details" when SKILL.md has none
- Add a `not_for` eval (a question about an existing graph goes to `/graphify`) and an eval where the user says no at the data-leaving prompt
- Make Phase 3 check for an existing `.gitignore` entry before appending, and make the writable check work before `graphify-out/` exists
- Add `reference/_implementation.md`, or rename `_workflow.md` to it, and add `output.returns` to the contract
- Replace the hardcoded `~/.claude/skills/graphify/` in `_troubleshooting.md` with a path built from the config directory
- Have the workflow run the checks in `_security.md` (symlink, umask, chmod, backup, checksum) or cut them, and make `stat -c` portable
- Fix the stale "v0.1.0 - Draft" evals header and the unpinned `pip install graphifyy` in `tests/README.md`

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 7/10 | 2026-10-27 | • 📐 **Sound:** five clear phases, detail in `reference/`, and a confirm before Phase 2<br>• 🌫️ **Undefined:** `_workflow.md` lists `--dry-run`, `--skip-extract` and `--state` "see SKILL.md", and nothing defines them<br>• ⚠️ **Contradiction:** `_examples.md` commits `graphify-out/graph.json` against the skill's own "Never" rule |
| **Complexity** | 5/10 | 2026-10-27 | • 🧮 **Raw complexity 5:** Concepts 2, Scope 1 (writes kept to the repo root), Dependencies 1 (`graphifyy` and an optional LLM backend), Prerequisites 1 (git and Python 3.8+)<br>• ✅ **Within the cap:** inside the tactical limit of 6, with a linear flow |
| **Test Coverage** | 6/10 | 2026-10-27 | • 📊 **Over range:** 15 prose evals, above tactical's 8–12, and nothing under `_tests/` runs them, so the cap of 7 applies<br>• 🕳️ **Gaps:** no eval for the `not_for` case or for declining the data-leaving prompt |
| **Code Quality** | 6/10 | 2026-10-27 | • ⚠️ **Writable check:** `touch graphify-out/.test` fails before the folder exists<br>• ⚠️ **Append:** `printf ... >> .gitignore` doesn't check first, so the FAQ's duplicate-detection and concurrent-run claims have nothing behind them<br>• ⚠️ **Regex:** the Python version check rejects 3.20 and later |
| **Security** | 7/10 | 2026-10-27 | • 🛡️ **Strong:** pinned `graphifyy==0.8.36`, an explicit yes before content goes to an LLM, no root, and writes kept to the repo root<br>• ⚠️ **Unused checks:** `_security.md` lists steps no phase runs, and `stat -c` is GNU-only<br>• ⚠️ **Leak risk:** the examples commit a graph that may hold LLM summaries of internal docs |
| **Documentation** | 7/10 | 2026-10-27 | • ✅ **Coverage:** SKILL.md, FAQ, troubleshooting and examples answer the expected questions<br>• 🍂 **Stale:** the examples commit `graph.json` and use the hyphenated branch `feature/add-graphify`<br>• ⚠️ **Drift:** the evals header says "v0.1.0 - Draft" against v1.2.2 tactical, and `tests/README.md` has an unpinned install |
| **Standards Compliance** | 6/10 | 2026-10-27 | • ✅ **Met:** naming, SKILL.md sections, a 1.2.2 header matching the contract, emoji headings and length<br>• ❌ **Missed:** no `reference/_implementation.md` (gate 6), no `output.returns` (gate 2) and a hardcoded `~/.claude/` path (gate 9)<br>• ⚠️ **Evals:** 15, above the tactical range |
| **Overall** | **6.3/10** | 2026-10-27 | The workflow is sound and the data-leaving safeguard is good, but reference files that contradict each other, flags nobody defined and unrun evals with no `not_for` case keep it below the tactical bar. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_setup_graphify/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_setup_graphify/tests/evals.yaml` — Test Coverage dimension
- `src/claude/_reference/_quality_scorecards/score_history.csv` — attempt 2, scored blind by `quality_scorecard_reviewer`
