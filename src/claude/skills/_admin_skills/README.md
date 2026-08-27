# ⚙️ Admin Skills

Maintenance and housekeeping workflows for the Claude setup itself.

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/archive_claude_config_snapshots` | Archive old `~/.claude_<timestamp>` snapshot directories based on age | 1.0.0 | [yes](../../../../tests/skills/_admin_skills/test_archive_claude_config_snapshots_skill.py) |
| `/sync_playbook` | Pull latest playbook changes and sync to both WSL and Windows Claude config | 1.0.0 | [yes](../../../../tests/skills/_admin_skills/test_sync_playbook_skill.py) |
| `/audit_agents` | Audit all Claude Code agents and produce a prioritised gap report | 0.1.0 | no |
| `/audit_skills` | Audit all installed skills in ~/.claude/skills/ and produce a prioritised gap report | 0.1.0 | [yes](../../../../tests/skills/_admin_skills/test_audit_skills_skill.py) |
| `/setup_graphify` | Set up Graphify on a repo to generate a local AST-based knowledge graph, reducing token cost for codebase exploration | 0.1.0 | [yes](../../../../tests/skills/_admin_skills/test_setup_graphify_skill.py) |
| `/review_claude_config` | Score the global Claude config out of 10 across six quality themes, produce a MoSCoW prioritisation, and optionally apply fixes | 0.1.0 | [yes](../../../../tests/skills/_admin_skills/test_review_claude_config_skill.py) |
