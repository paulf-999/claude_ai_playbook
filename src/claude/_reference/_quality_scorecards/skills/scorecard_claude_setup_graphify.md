# Quality Scorecard — claude_setup_graphify

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-06

**Overall score:** 8.4/10

**Recommended improvements:**
- Bring the evals within the tactical range of 8–12, or justify strategic maturity

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 10/10 | 2026-09-07 | • ✅ **Workflow:** pre-flight checks, five clear phases, and `--dry-run`, `--skip-extract` and `--state` options |
| **Complexity** | 4/10 | 2026-10-06 | • 🧮 **Raw complexity 6:** five phases (Concepts 2), one repo (Scope 1), the `graphifyy` package and an LLM extraction (Dependencies 2), git, Python and write checks (Prerequisites 1) |
| **Test Coverage** | 8/10 | 2026-10-06 | • 📊 **Count:** 15 structured evals covering checks, happy paths and errors<br>• ⚠️ **Range:** above the tactical range of 8–12, and nothing runs them |
| **Code Quality** | 9/10 | 2026-10-06 | • ✅ **Checks:** validates the repo, Python version and write access first, and the install check imports the real `graphify` module<br>• ✅ **Commands:** every `graphify` command and flag matches the 0.8.36 help, including `extract .` and `update .` |
| **Security** | 9/10 | 2026-10-06 | • ✅ **Pinned:** installs `graphifyy==0.8.36` in every command and the contract<br>• ✅ **Data leaving the machine:** `_security.md` says code stays local and docs get an LLM pass, and extraction waits for the user's yes<br>• ⚠️ **Unverified:** a fully offline run and a `pip-audit` check haven't been done |
| **Documentation** | 10/10 | 2026-10-06 | • ✅ **Reference:** workflow and FAQ, troubleshooting, security and examples<br>• ✅ **SKILL.md:** 60 lines, linking the real Graphify project |
| **Standards Compliance** | 9/10 | 2026-10-06 | • ✅ **Hard gates:** Instructions for Claude before Purpose, off the baseline, five sections and 60 lines<br>• ⚠️ **Evals:** 15, above the tactical range of 8–12 |
| **Overall** | **8.4/10** | 2026-10-06 | A well-designed, pinned and transparent setup flow that meets the SKILL.md standard, held back by its real complexity and an over-range eval count. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_setup_graphify/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_setup_graphify/tests/evals.yaml` — Test Coverage dimension
