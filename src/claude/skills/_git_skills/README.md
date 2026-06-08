# 🛠️ Git Skills

Git and GitHub workflow skills.

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/git_create_pr` | Full PR workflow — branch, stage, commit, push, and open a GitHub PR following team conventions | 1.3.0 | [yes](../../../../tests/skills/_git_skills/test_git_create_pr_skill.py) |
| `/git_notify_pr` | Post a Teams channel notification after raising a PR, resolving reviewers from the DPE team mapping | 1.1.0 | [yes](../../../../tests/skills/_git_skills/test_git_notify_pr_skill.py) |
| `/git_review_pr` | Generate and post a structured Claude review comment on a GitHub PR with a scored scorecard | 0.2.0 | [yes](../../../../tests/skills/_git_skills/test_git_review_pr_skill.py) |
| `/git_request_changes_pr` | Post a formal GitHub CHANGES_REQUESTED review with inline file comments anchored to specific files and lines | 0.3.1 | [yes](../../../../tests/skills/_git_skills/test_git_request_changes_pr_skill.py) |
