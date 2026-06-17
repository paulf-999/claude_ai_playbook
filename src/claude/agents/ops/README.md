# ⚙️ Agents — Ops

Agents for maintaining and validating the Claude setup itself. Read-only access.

| File | Agent name | Purpose |
|------|------------|---------|
| [`claude_reviewer.md`](claude_reviewer.md) | `claude_reviewer` | 🏅 Review Claude configuration artefacts for quality, clarity, and best practices compliance |
| [`mac_user.md`](mac_user.md) | `mac_user` | 🍎 Review shell scripts for macOS compatibility issues (bash 3.2, BSD coreutils, missing tools) |
| [`new_user.md`](new_user.md) | `new_user` | 🆕 Test the Claude onboarding experience by simulating a first-time user following the setup docs |
| [`skill_auditor.md`](skill_auditor.md) | `skill_auditor` | 🔍 Audit all installed skills in ~/.claude/skills/ and produce a prioritised gap report |
