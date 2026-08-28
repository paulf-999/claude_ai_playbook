# 🧪 Settings Tests

Quality assurance for configuration files: `aliases.md`, `settings.json`, and related documentation.

---

## Test Suites

### `test_aliases.py`

Validates `src/claude/aliases.md` table entries:

- ✅ All required fields present (Input, Theme, Status, Meaning)
- ✅ Status is valid (Ready, Testing)
- ✅ No duplicate alias inputs
- ✅ Meaningful descriptions (>10 chars)
- ✅ Input format is correct (/command or bare_word)
- ✅ All aliases are documented
- ✅ Automation aliases reference control docs

**Run:**
```bash
python3 src/claude/_tests/settings/test_aliases.py
```

---

### `test_aliases_behavior.py`

**Integration tests** — validates that aliases actually work as described:

- ✅ Skills exist (check `src/claude/skills/`) or are built-in Claude Code commands
- ✅ Conventions are documented in rules
- ✅ Meaning descriptions match actual behavior (spot-checks)
- ✅ All aliases are executable/callable or documented

Tests both:
- **Skills/Commands** (e.g., `/fewer-permission-prompts`, `/plan`) — verifies skill files exist or command is built-in
- **Conventions** (e.g., `bullets`, `draft`) — verifies documented in `_rules/writing_style.md`

**Run:**
```bash
python3 src/claude/_tests/settings/test_aliases_behavior.py
```

**Example output:**
```
✅ /batch                         | ✅ Built-in command: batch automation
✅ bullets                        | ✅ Documented in _rules/writing_style.md
✅ /fewer-permission-prompts      | ✅ Documented command: transcript auditing
✅ plan                           | ✅ Meaning matches behavior
```

---

### `test_settings.py`

Validates `src/claude/settings.json` and enforces guiding principles:

- ✅ Valid JSON structure
- ✅ Required top-level keys exist
- ✅ No redundant/duplicate entries
- ✅ Every setting documented in `settings.json.README.md`
- ✅ Settings align with guiding principles
- ✅ Total context cost is reasonable (<500 tokens)

**Run:**
```bash
python3 src/claude/_tests/settings/test_settings.py
```

**Framework for proposing new settings:**

When proposing a new setting to `settings.json`, use `propose_new_setting()`:

```python
from test_settings import propose_new_setting

approved, reason = propose_new_setting(
    name='features.myFeature',
    value=True,
    justification='Solves X problem by doing Y. Observed Z times/week.',
    estimated_tokens=50,  # Budget: <200
    principles_alignment=[
        'explicit_over_implicit',  # Why this setting
        'context_efficiency',       # Why not more context bloat
        'reversible',               # Why easy to remove
    ]
)

if approved:
    print(f"✅ Approved: {reason}")
else:
    print(f"❌ Rejected: {reason}")
```

**Approval criteria:**

1. **Token cost <200** — no setting should consume excessive context
2. **Align with ≥2 principles** — must be intentional + efficient
3. **Clear justification** — explain the problem and solution
4. **Document in README** — add entry to `settings.json.README.md`

---

## Guiding Principles

All settings must align with these (see `_rules/guiding_principles.md`):

| Principle | Means | Example |
|-----------|-------|---------|
| **Lazy-load** | Don't auto-inject | Settings are read once; not injected on every prompt |
| **Explicit** | Visible choice, not magic | `defaultMode: "plan"` = user approval before changes |
| **Context efficient** | Every token counts | Permission allowlist reduces friction, not bloat |
| **Intentional** | Solve real problems | Settings exist because of observed usage, not speculation |
| **Reversible** | Easy to add/remove | Disabled plugins in `_wip/` for easy restoration |

---

## Adding a New Test

If adding a new settings-related file (e.g., `hooks.json`, `agents.json`):

1. Create a new test file: `test_<name>.py`
2. Implement validation tests (structure, required fields, principles alignment)
3. Add token cost estimation
4. Document in this README
5. Run tests in CI/CD pipeline

---

## CI/CD Integration

These tests should run on every PR to `src/claude/`:

```bash
python3 -m pytest src/claude/_tests/settings/ -v
```

Or manually:

```bash
python3 src/claude/_tests/settings/test_aliases.py && \
python3 src/claude/_tests/settings/test_settings.py
```
