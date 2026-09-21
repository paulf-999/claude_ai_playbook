# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `claude_capture_session_prompts` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `capture_default_date` | Capture | Captures today's prompts into a dated markdown table with summary stats |
| 2 | `capture_specific_date` | Capture | `--date` captures only the requested past date's prompts |
| 3 | `categorization_themes` | Categorize | Theme column (Rules, Skills, Process, Planning, TODOs, etc.) is accurate |
| 4 | `categorization_status` | Categorize | Status markers (Done, Pending, Question, Response, Note) are detected correctly |
| 5 | `markdown_table_format` | Output | The generated table is well-formed, complete, and not truncated |
| 6 | `manual_refinement_workflow` | Integration | The output file can be hand-edited and re-read for TODO planning |

- **No Python handler:** this skill has none
- **Only coverage:** `evals.yaml` is this skill's sole test coverage
