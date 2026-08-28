# Testing

Structural validation tests run automatically on every commit (via pre-commit hook) and on every PR touching `src/claude/` (via GitHub Actions).

---

## What is tested

| Test module | What it covers |
|---|---|
| `test_agents.py` | Valid frontmatter, required sections, `EnterPlanMode` present |
| `test_skills.py` | `SKILL.md` exists, valid frontmatter, name matches directory, file references resolve |
| `test_process.py` | Required process files exist, key content present (`EnterPlanMode`, `## Sub-agent`, `## Task`) |
| `test_commands.py` | Command files non-empty, README links resolve |
| `test_rules.py` | Rule files non-empty, README links resolve |
| `test_style_guide_standards.py` | `@import` references resolve, child page table links exist |

---

## Running tests locally

```bash
make deps    # install test dependencies (first time only)
make test    # run the full test suite
```

---

## Pre-commit hook

The targeted test hook runs automatically on commit. It detects which files are staged and runs only the relevant test module — not the full suite. No configuration needed after `pre-commit install`.
