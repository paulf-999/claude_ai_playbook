# 🛠️ Maintenance script tests

Unit tests for the standalone Python scripts in `src/sh/claude/`.

---

## 💡 What these tests are

- Scripts invoked via `make lint_tags` and `make audit_components`
- Not Claude components — repo maintenance tools
- Standard unit tests: call a function, assert the output

---

## ➕ Adding a new tooling test file

Create `tests/tooling/test_<script_name>.py` when adding a new script to `src/sh/claude/`.

---

## 📄 Files

| File | Script | What it covers |
|---|---|---|
| `test_claude_component_audit.py` | `claude_component_audit.py` | Health signal detection (`check_health`) and file discovery (`find_all_components`) |
| `test_claude_tag_lint.py` | `claude_tag_lint.py` | Validation logic (`validate_component`) and file discovery (`find_components`) |
