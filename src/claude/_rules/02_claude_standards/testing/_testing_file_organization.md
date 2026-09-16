# 📍 Test File Organization

**Purpose:** Establish clear structure for where tests live and how to organize them.

---

## Structure Pattern

**Rule:** Place tests adjacent to the code they test.

```
~/.claude/
├── aliases.md
├── settings.json
├── _rules/
│   └── testing.md  (this file)
└── _tests/
    └── settings/
        ├── test_aliases.py          (validates aliases.md structure)
        ├── test_aliases_behavior.py (validates alias behavior)
        ├── test_settings.py         (validates settings.json + principles)
        └── README.md                (test documentation)
```

---

## Naming Convention

| Artifact | Test File | Purpose |
|---|---|---|
| `aliases.md` | `test_aliases.py` | Structure validation |
| `_rules/<tier>/<file>.md` | `test_<file>.py` | Structural validation (existence, sections, patterns) |
| Feature behavior | `test_<feature>_behavior.py` | Functional testing |
| Principles alignment | `test_<feature>_principles.py` | Compliance validation |
| End-to-end | `test_<feature>_integration.py` | System integration |

**Pattern:** `_tests/<domain>/test_<feature>[_<aspect>].py`

**Rule/hook structural tests must mirror their target filename.** When a test
validates a single `_rules/` or `hooks/` file's structure (existence, required
sections, content patterns), name the test file after that target, not after
a paraphrase of what it does.

- **Drop the leading underscore** on child files: `_decision_making.md` → `test_decision_making.py`, not `test__decision_making.py` or `test_decision_making_rule.py`.
- **Don't repeat the tier/domain in the filename** — the test's own subdirectory placement (mirroring `_rules/`'s tier structure, e.g. `_tests/rules/02_claude_standards/`) already carries that context. `git.md` → `test_git.py`, not `test_02_claude_standards_git.py` or `test_git_rules.py`.
- **When there's no single target file** (the test validates a pattern across a whole tier or directory, not one file's content), name it for what it validates instead — e.g. `test_lazy_load_coverage.py`, `test_rules_structure.py` — and leave it out of the tier subdirectories.

**Why:** A reader scanning `_tests/rules/02_claude_standards/` should be able to tell which `_rules/` file each test covers without opening it. Names that paraphrase ("rule", "compliance", "behavior") drift from the target over time and stop matching after a rename — the file itself doesn't.

---

## Creating New Tests

For new feature: create `_tests/<domain>/test_<feature>.py` with clear goal statement.

**Example structure:**
```python
# _tests/skills/test_git_create_pr.py

def test_git_create_pr_structure():
    """Validates skill.contract.yaml has all required fields."""
    # Test code here

def test_git_create_pr_behavior():
    """Verifies skill creates valid PR with populated description."""
    # Test code here

def test_git_create_pr_naming():
    """Ensures skill name follows domain_action pattern."""
    # Test code here
```

**Principle:** One goal per test function; descriptive name explains what's being validated.
