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
| Feature behavior | `test_<feature>_behavior.py` | Functional testing |
| Principles alignment | `test_<feature>_principles.py` | Compliance validation |
| End-to-end | `test_<feature>_integration.py` | System integration |

**Pattern:** `_tests/<domain>/test_<feature>[_<aspect>].py`

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
