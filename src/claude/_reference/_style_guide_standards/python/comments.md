<!-- version: 1.0.0 -->
<!-- created: 2026-10-02 -->
<!-- updated: 2026-10-02 -->
# 💬 Python Inline Comments

**Purpose:** Say when and how to comment Python code, so readers can follow it without pausing.

---

Comments reduce cognitive load — err on the side of over-commenting rather than under-commenting.

- **Non-obvious logic:** anything a reader would need to pause to understand
- **Non-trivial conditionals:** explain the purpose, not just mechanics
- **Fallback behaviour:** constraints not apparent from code
- **Logical phases:** label distinct steps in functions longer than ~10 lines
- **`TODO` / `FIXME`:** always include brief explanation of what and why
  - **Placement:** always above the code they describe — never at end of line
  - **Accuracy:** keep comments accurate — stale comments are worse than none
  - **No restatement:** do not restate obvious code (e.g., `i += 1  # increment i`)

Also label groups of related module-level constants:

```python
# The four possible actions a planned change can resolve to
CREATE = "CREATE"
UPDATE = "UPDATE"
DISABLE = "DISABLE"
NOOP = "NOOP"
```
