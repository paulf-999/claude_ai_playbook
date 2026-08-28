# 📋 File Structure Validation

**Purpose:** Instruct Claude to validate `~/.claude/` naming and structure compliance after creating or modifying files, ensuring consistency and preventing configuration drift.

## 🎯 When to validate

Automatically validate file structure after:
- Creating new files or directories in `~/.claude/`
- Renaming files or directories
- Moving files between directories
- Deleting files or directories

**Note:** This is automatic behavior — Claude should validate without being asked.

---

## 🔧 How to validate

Run the compliance test after any file/directory changes:

```bash
python3 ~/.claude/_tests/test_file_structure_compliance.py
```

**What it checks:**
- ✅ **Snake_case naming** — all files and directories use lowercase letters, numbers, underscores only
- ✅ **Underscore prefixes** — user-created directories (`_rules/`, `_tests/`, etc.) start with underscore; auto-generated directories (`memory/`, `backups/`, etc.) do not
- ✅ **Child file naming** — files within a subdirectory start with underscore (e.g., `_child_file.md`)
- ✅ **Directory placement** — `_rules/`, `_tests/`, etc. are only at top level of `~/.claude/`
- ✅ **File placement** — root-level files are only at top level (e.g., `CLAUDE.md`, `settings.json`)

**Violation severity:**
- **Errors** (violations found) — Fix before proceeding
- **OK** (all compliant) — Safe to proceed

---

## 📝 Failure recovery

**If the test reports violations:**

1. **Read the violation message** — it indicates exactly what's wrong (naming, placement, prefix)
2. **Fix the issue** — rename, move, or delete the file as indicated
3. **Re-run the test** — verify the fix resolves the violation
4. **If unsure,** refer to `~/.claude/_rules/01_essentials/conventions/claude_directory_structure.md` for authoritative naming and placement rules

**Example violation and fix:**
```
❌ my_new_file.md: child file in _rules/ should start with underscore (e.g., _filename.md)

Fix: Rename _rules/my_new_file.md → _rules/_my_new_file.md
```

---

## 🔗 Related rules

- `claude_directory_structure.md` — Authoritative naming and placement rules
- `naming_standards.md` — Foundational naming principles
- `behaviour.md` → "Before acting" → "Plan approval" — validate structure before proceeding with complex changes

---
