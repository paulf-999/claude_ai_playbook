---
created: 2025-11-15
last_modified: 2026-08-19
---

# 🧪 Testing Strategy

Detailed guide to test coverage, test layers, and integration patterns in the Claude config.

---

## Test layers

Tests are organized into four independent layers, each validating a different concern:

| Test layer | What it validates | Location | Examples |
|---|---|---|---|
| **Structure** | Files follow format constraints | `_tests/rules/test_rules_structure.py` | Line limits (<110), trailing newlines, emoji headers |
| **Behavior** | Features work as documented | `_tests/rules/test_*.py` | Aliases callable, rules consistent, automation controls gate correctly |
| **Compliance** | Config aligns with principles | `_tests/settings/test_settings.py` | No lazy-load imports in CLAUDE.md, permissions valid, intentionality |
| **Integration** | Hooks register and fire correctly | `_tests/hooks/test_hook_registry.py` | Enforcement hooks execute, style guide hooks inject context |

---

## Structure tests

**Goal:** Ensure all files follow format constraints.

**Coverage:**
- All `_rules/` files under 110 lines
- All `_reference/` files under 110 lines (or properly split into parent + children)
- All files end with trailing newline
- All major headings have emoji prefix

**Why it matters:** Consistent format reduces cognitive load and makes content scannable.

**File:** `_tests/rules/test_rules_structure.py` (~150 lines)

---

## Behavior tests

**Goal:** Validate that features work as documented.

**Coverage by feature:**

| Feature | Test file | What's validated |
|---|---|---|
| Aliases | `test_aliases_behavior.py` | Aliases are callable; `/alias_name` runs the referenced command |
| Automation controls | `test_automation_controls.py` | `/loop`, `/batch`, `/goal` gates and turn budgets work |
| Guiding principles | `test_guiding_principles.py` | Lazy-load rules aren't imported at top level; intentionality criteria met |
| Git workflow | (inline in git.md tests) | Commit messages follow format; branch naming valid |

**Example:** The `/loop` command has a 10-minute minimum interval — `test_automation_controls.py` verifies this constraint is enforced.

---

## Compliance tests

**Goal:** Ensure config aligns with guiding principles.

**Coverage:**

| Principle | Test | Validated |
|---|---|---|
| **Lazy-load by default** | `test_guiding_principles.py` | Domain-specific rules in `lazy_load/`, not top-level |
| **Explicit over implicit** | Manual audit (no automation) | Every import commented in CLAUDE.md |
| **Context efficiency** | `test_settings.py` | Baseline token cost tracked; large imports flagged |
| **Intentionality** | Manual review during PR | Features solve real problems; usage evidence provided |
| **Reversible by design** | Manual spot-checks | Rules are single-purpose; can be removed without side effects |

**Example:** When a new top-level import is proposed, `test_guiding_principles.py` fails until the import is documented with its token cost and justification.

---

## Integration tests

**Goal:** Validate that hooks register, execute, and inject context correctly.

**Coverage:**

| Hook type | Test file | What's validated |
|---|---|---|
| Dispatcher hooks | `test_hook_registry.py` | Hook is registered; calls all child hooks; aggregates output |
| Enforcement hooks | `test_enforcement_*.py` | Hook enforces the rule; blocks/warns on violations |
| Style guide hooks | `test_style_guide_*.py` | Hook injects context on-demand; doesn't run baseline |

**Example:** When a new enforcement hook is added (e.g., `hook_enforcement_sql_formatting.sh`), the test suite verifies:
1. Hook is registered in settings.json
2. Hook correctly identifies violations (e.g., unformatted SQL)
3. Hook warns the user with clear messaging

---

## Test coverage summary

**16 test files, 1,277+ lines of test code:**

```
_tests/
├── rules/
│   ├── test_rules_structure.py           (~150 lines)
│   ├── test_guiding_principles.py        (~100 lines)
│   ├── test_aliases_behavior.py          (~80 lines)
│   ├── test_automation_controls.py       (~120 lines)
│   └── [additional tests per domain]
│
├── hooks/
│   ├── test_hook_registry.py             (~100 lines)
│   ├── test_enforcement_naming.py        (~80 lines)
│   ├── test_enforcement_testing.py       (~80 lines)
│   ├── test_style_guide_sql.py           (~90 lines)
│   └── [additional tests per hook]
│
├── settings/
│   └── test_settings.py                  (~90 lines)
│
└── README.md
```

**Coverage goals by maturity:**
- Draft: structure + basic behavior tests
- Tactical: structure + behavior + one compliance test
- Strategic: all four layers fully covered

---

## Adding tests for new features

### 1. New rule or hook

Create corresponding test file:
```
_tests/rules/test_<feature_name>.py     # For rules
_tests/hooks/test_<feature_name>.py     # For hooks
```

Validate:
- Structure (file size, format)
- Behavior (feature works as documented)
- Compliance (aligns with principles)

### 2. New skill

Add test to `_tests/skills/`:
```
_tests/skills/test_<skill_name>.py
```

Validate:
- Skill invocable via `/skill_name`
- Contract fields present (name, version, maturity, etc.)
- Workflow executes without errors

### 3. Settings changes

Update `test_settings.py`:
- New permission? Validate it's least-privilege
- New hook registration? Validate it's safe
- New baseline import? Validate token cost and justification

---

## Related documents

- **Test documentation:** `~/.claude/_tests/README.md`
- **Testing rules:** `~/.claude/_rules/testing.md`
- **Parent doc:** `claude_config_architecture.md`
