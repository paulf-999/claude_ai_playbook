<!-- version: 2.0.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
# ⚠️ Common Mistakes

**Purpose:** The most frequent skill-authoring mistakes and their fixes, including the security gaps every skill must avoid.

---

## Common Mistakes to Avoid

**❌ Mistake 1: Too much detail in SKILL.md**
```markdown
## Purpose
This skill creates Confluence pages with formatting, validation, error handling,
retry logic, permission checking, and extensive documentation...
[continues for 80+ lines]
```
**✅ Fix:** Externalize to reference files
- Keep SKILL.md to ~60 lines
- Move implementation details to `reference/_implementation.md`
- Move format specs to `reference/_formats.md`

**❌ Mistake 2: Vague purpose statement**
```markdown
## Purpose
Do Confluence stuff
```
**✅ Fix:** Be specific and user-focused
```markdown
## Purpose
Create Confluence pages with auto-populated templates and validation:
- **Template-based creation** — Use pre-built page templates
- **Field validation** — Ensure required fields are populated
- **Error recovery** — Handle invalid inputs gracefully
```

**❌ Mistake 3: Missing scope boundaries**
```yaml
dispatch:
  not_for: []  # Empty! Undefined scope, will bloat over time
```
**✅ Fix:** Be explicit about what you DON'T do
```yaml
dispatch:
  not_for:
    - Page editing or updating (use /confluence_update_page)
    - Permission management (separate skill)
    - Deleting pages (intentionally excluded for safety)
```

**❌ Mistake 4: No maturity justification**
```yaml
maturity: tactical
# No evidence, no explanation
```
**✅ Fix:** Add one sentence to SKILL.md's Best For line, choosing the stage from the maturity table in `_core_standards.md`
```markdown
**Best for:** One-off pages using the general_page pattern. Currently at the
**tactical** stage — main path plus light error handling, not full edge-case coverage yet.
```

**❌ Mistake 5: Security gaps**
- ✅ **Secrets:** use environment variables only, and list them in `requires.resources`.
- ✅ **Inputs:** validate user input before it reaches an API or shell command.
- ✅ **Permissions:** request only what's needed, and list each one in `dependencies.permissions`.
- ✅ **Errors:** give a clear fix-it message, never a stack trace.
- **Note:** the full standard lives in `security.md`.

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
- Sibling: `_core_standards.md` — maturity table and where to justify the chosen level
