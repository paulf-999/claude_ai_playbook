# 🔧 Agents — Utility

Read-only review and diagnostic agents. Generally restricted to `Read, Glob, Grep`. Exception: `agent-auditor` includes `Write, Edit` solely to maintain its persistent memory files — it never modifies agent source files.

| File | Agent name | Purpose |
|------|------------|---------|
| [`code_reviewer.md`](code_reviewer.md) | `code_reviewer` | 🔍 Review code, PRs, and diffs for correctness, standards, security, and test coverage |
| [`debugger.md`](debugger.md) | `debugger` | 🐛 Diagnose errors, pipeline failures, unexpected behaviour, and data quality issues |
| [`agent-auditor.md`](agent-auditor.md) | `agent-auditor` | 📋 Audit all Claude Code agents and produce a prioritised gap report — read-only |
