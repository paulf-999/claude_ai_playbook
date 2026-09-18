# ⚠️ Common Mistakes & Security

**Purpose:** The most frequent skill-authoring mistakes and their fixes, plus the security considerations every skill must address.

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
**✅ Fix:** Document why this level
```markdown
## Maturity Justification

**Real problem solved:** Teams repeatedly create Confluence pages from templates.

**Use frequency:** Used in 12% of sessions, 3-4 times per week in active projects.

**Test coverage:** 15 evals covering template selection, validation errors, API failures.

**Dependency assessment:** Confluence API is stable; no experimental tools.

**Scope assessment:** Clear boundaries; v1.0 = creation only. Editing deferred to v2.0.

**Conclusion:** Justifies Tactical maturity because:
- Real, recurring problem (template creation)
- 15 evals cover all phases (Tactical requirement)
- Stable external dependency (Confluence API)
- Clear boundaries prevent scope creep
```

## Security Considerations [IMPORTANT]

When authoring skills, prioritize security:

**Secrets & Credentials**
- ❌ Never hardcode API keys, tokens, or passwords
- ✅ Use environment variables only (e.g., `SLACK_BOT_TOKEN`, `JIRA_TOKEN`)
- ✅ Document required env vars in `requires.resources` section

**Input Validation**
- ❌ Don't pass user input directly to APIs or shell commands
- ✅ Validate all inputs against expected format (length, type, allowed chars)
- ✅ Reject suspicious patterns (command injection, path traversal, etc.)

**Permissions & Least Privilege**
- ❌ Don't request more permissions than needed
- ✅ List required permissions in `dependencies.permissions` (e.g., `chat:write`, `channels:read`)
- ✅ Document why each permission is needed

**Error Messages**
- ❌ Don't expose internal details or stack traces
- ✅ Provide clear, user-friendly error messages
- ✅ Guide users on how to fix the issue (e.g., "Set SLACK_BOT_TOKEN environment variable")

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
