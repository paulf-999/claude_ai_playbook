# 🛠️ Git Skills

Git and GitHub workflow skills.

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/create_pr` | Full PR workflow — branch, stage, commit, push, and open a GitHub PR following team conventions | 1.2.0 | [yes](../../../../tests/skills/_git_skills/test_create_pr_skill.py) |
| `/notify_pr` | Post a Teams channel notification after raising a PR, resolving reviewers from the DPE team mapping | 1.0.0 | [yes](../../../../tests/skills/_git_skills/test_notify_pr_skill.py) |
| `/git_review_pr` | Generate and post a structured Claude review comment on a GitHub PR with a scored scorecard | 0.2.0 | [yes](../../../../tests/skills/_git_skills/test_git_review_pr_skill.py) |
| `/request_changes_pr` | Post a formal GitHub CHANGES_REQUESTED review with inline file comments anchored to specific files and lines | 0.3.1 | [yes](../../../../tests/skills/_git_skills/test_request_changes_pr_skill.py) |
