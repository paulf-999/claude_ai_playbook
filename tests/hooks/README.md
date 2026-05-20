# 🪝 Claude hook tests

Unit tests for Claude hook scripts in `src/claude/hooks/`.

---

## 💡 What these tests are

- Hooks are Python scripts that execute in response to Claude lifecycle events
- Unlike skills, they contain real, importable Python logic
- Standard unit tests: call a function, assert the output

---

## ➕ Adding a new hook test file

Create `tests/hooks/test_<hook_name>.py` when adding a new hook to `src/claude/hooks/`.

---

## 📄 Files

| File | Hook | What it covers |
|---|---|---|
| `test_claude_prompt_reviewer.py` | `claude_prompt_reviewer` | All check functions, output building, and the full `emit_output` paths (pass, low severity, high severity) |
