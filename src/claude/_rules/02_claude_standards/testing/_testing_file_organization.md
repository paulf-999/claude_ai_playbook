# 📍 Test File Organisation

**Purpose:** Establish clear structure for where tests live and how to organise them.

---

## 🔀 Colocate vs. Centralise

Not every test belongs in `_tests/`. Choose based on what's being tested, not habit:

- **Colocate inside the artifact** when the test is tightly coupled to that one artifact's content or behaviour, and its primary audience is whoever maintains that artifact — e.g. a skill's `tests/evals.yaml` lives inside `skill_name/tests/`, not `_tests/skills/`.
- **Centralise in `_tests/`** when the test needs a uniform sweep across many artifacts, shares fixtures/utilities, or only makes sense in aggregate — e.g. `test_no_orphaned_skill_files.py` scans every skill at once and couldn't live inside any single one.

**Why:** forcing one pattern universally either duplicates cross-cutting logic per artifact (all-colocated) or buries artifact-specific behaviour tests where nobody browsing that artifact would find them (all-centralised).

**Both apply within one artifact type:** skills demonstrate this directly — `evals.yaml` colocates inside each skill's own `tests/` folder, while `test_no_orphaned_skill_files.py` and `test_skill_structure_compliance.py` live centrally because they validate properties across all skills at once.

**Caveat — spec files aren't code test files:** this principle was demonstrated with `evals.yaml`, a content/spec file with no test-runner dependency — moving it has zero tooling cost. A `.py` pytest module is different: it depends on shared collection config (`pytest.ini`'s `testpaths`, `pythonpath`, coverage setup), so relocating it changes shared infrastructure, not just a file's address. Don't extend "colocate when tightly coupled" to pytest files without also checking whether the test runner would still find them — see `authoring_skills.md` → `_scope_and_maintenance.md` for when a skill should have a `test_*_handler.py` file at all.

---

## Structure Pattern

**Rule:** Everything that isn't colocated per the section above goes in `_tests/`, adjacent (by domain) to the code it tests.

```
~/.claude/
├── aliases.md
├── settings.json
├── _rules/
│   └── testing.md  (this file)
└── _tests/
    └── settings/
        ├── test_aliases.py          (validates aliases.md structure)
        ├── test_aliases_behavior.py (validates alias behaviour)
        ├── test_settings.py         (validates settings.json + principles)
        └── README.md                (test documentation)
```

---

## Naming Convention

| Artifact | Test File | Purpose |
|---|---|---|
| `aliases.md` | `test_aliases.py` | Structure validation |
| `_rules/<tier>/<file>.md` | `test_<file>.py` | Structural validation (existence, sections, patterns) |
| Feature behaviour | `test_<feature>_behavior.py` | Functional testing |
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
