# ⚙️ Admin Skills

Maintenance and housekeeping workflows for the Claude setup itself.

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/archive_claude_config_snapshots` | Archive old `~/.claude_<timestamp>` snapshot directories based on age | 1.0.0 | [yes](../../../../tests/skills/_admin_skills/test_archive_claude_config_snapshots_skill.py) |
| `/sync_playbook` | Pull latest playbook changes and sync to both WSL and Windows Claude config | 1.0.0 | [yes](../../../../tests/skills/_admin_skills/test_sync_playbook_skill.py) |
| `/audit_agents` | Audit all Claude Code agents and produce a prioritised gap report | 0.1.0 | no |
