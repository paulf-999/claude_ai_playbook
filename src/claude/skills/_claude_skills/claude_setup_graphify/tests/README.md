# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `claude_setup_graphify` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `validate_git_repo` | Pre-flight | Confirms a git repository, and fails gracefully outside one |
| 2 | `validate_python_version` | Pre-flight | Confirms Python 3.8+, and fails gracefully on 3.6/3.7 |
| 3 | `validate_writable_directory` | Pre-flight | Confirms the target directory is writable, and fails gracefully if it's read-only |
| 4 | `install_graphify` | Install | Pinned `pip install "graphifyy==0.8.36"`, then `graphify install --platform claude`, succeed |
| 5 | `extract_knowledge_graph` | Extract | `graphify extract .` generates `graph.json` after the user confirms what leaves the machine |
| 6 | `add_gitignore_entry` | Extract | `graphify-out/` gets appended to `.gitignore` |
| 7 | `update_claude_md` | Extract | `CLAUDE.md` gets a Graphify section added |
| 8 | `verify_graphify_skill_callable` | Verify | `/graphify` answers a structural question without reading files directly |
| 9 | `error_install_fails` | Errors | A failed install/pip step gives a clear error with a retry suggestion |
| 10 | `error_extraction_fails` | Errors | A failed extraction reports the error with a retry suggestion |
| 11 | `error_skill_not_callable` | Errors | A failed `/graphify` verification is detected, suggests manual check |
| 12 | `query_existing_graph_out_of_scope` | Not for | A question about an existing graph is sent to `/graphify` |

- **No Python handler:** this skill has none
- **Only coverage:** `evals.yaml` is this skill's sole test coverage
