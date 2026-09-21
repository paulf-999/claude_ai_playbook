# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `claude_setup_graphify` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `validate_git_repo` | Pre-flight | Confirms the current directory is a git repository |
| 2 | `validate_not_git_repo` | Pre-flight | Fails gracefully with a clear message if not in a git repo |
| 3 | `validate_python_version` | Pre-flight | Confirms Python 3.8+ is available |
| 4 | `validate_python_too_old` | Pre-flight | Fails gracefully on Python 3.6/3.7 |
| 5 | `validate_writable_directory` | Pre-flight | Confirms the target directory is writable |
| 6 | `validate_readonly_directory` | Pre-flight | Fails gracefully if the target directory is read-only |
| 7 | `install_graphifyy_package` | Install | `pip install graphifyy` succeeds |
| 8 | `install_graphify_claude_skill` | Install | `graphify install --platform claude` succeeds |
| 9 | `extract_knowledge_graph` | Extract | `graphify extract` generates `graph.json`, notes the cost |
| 10 | `add_gitignore_entry` | Extract | `graphify-out/` gets appended to `.gitignore` |
| 11 | `update_claude_md` | Extract | `CLAUDE.md` gets a Graphify section added |
| 12 | `verify_graphify_skill_callable` | Verify | `/graphify` answers a structural question without reading files directly |
| 13 | `error_install_fails` | Errors | A failed install/pip step gives a clear error with a retry suggestion |
| 14 | `error_extraction_fails` | Errors | A failed extraction reports the error with a retry suggestion |
| 15 | `error_skill_not_callable` | Errors | A failed `/graphify` verification is detected, suggests manual check |

- **No Python handler:** this skill has none
- **Only coverage:** `evals.yaml` is this skill's sole test coverage
