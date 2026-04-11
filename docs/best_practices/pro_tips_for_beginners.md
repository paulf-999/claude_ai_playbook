# 💡 Pro tips for beginners

Four quick habits from Anthropic's quickstart guide that improve results from day one.

Source: [Anthropic Claude Code Quickstart — Pro tips for beginners](https://code.claude.com/docs/en/quickstart#pro-tips-for-beginners)

| Tip | Description | Example |
|---|---|---|
| 🎯 Be specific with your requests | Include model paths, column names, and constraints upfront. Precise instructions reduce corrections. | [prompt examples](#be-specific-examples) |
| 📋 Use step-by-step instructions | For complex tasks, break them into an explicit sequence rather than asking for everything at once. | Instead of `"Refactor the Access One staging models, add tests, and update the YAML docs"` — try `"First, refactor staging_access_one_merchant_list.sql. Once I've confirmed that looks right, we'll update the tests."` |
| 🔍 Let Claude explore first | Ask Claude to read and explain code before making changes. Prevents solving the wrong problem. | `"Read prod_analytics/models/staging/salesforce/ and explain how deduplication works — don't change anything yet."` |
| ⌨️ Save time with shortcuts | Built-in shortcuts reduce friction for common interactions. | [shortcut reference](#shortcuts-reference) |

---

## 💻 Code examples

### 🎯 Be specific — prompt examples

| Vague | Specific |
|---|---|
| `"fix the dbt model"` | `"mart_payroc_commerce_payouts is producing duplicate rows — check the grain in base/access_one/access_one_merchant_list.sql and add unique + not_null tests to KEY"` |
| `"add a staging model"` | `"create staging_salesforce_opportunity.sql following the pattern in staging_salesforce_merchant_list.sql — rename columns to snake_case and add audit fields via {{ dbt_last_modified_field() }}"` |
| `"debug the DAG failure"` | `"parent_dag_salesforce_hourly is failing on tg_dbt_run_staging_base_tasks — read the last failed run logs and add a retry to the Docker operator"` |

Reference specific file paths and column names. Name the constraint upfront — what Claude should follow, what it should avoid, and what "done" looks like.

---

### ⌨️ Shortcuts reference

| Shortcut | What it does |
|---|---|
| `! <command>` | Run a shell command from the Claude prompt — e.g. `! dbt compile` or `! dbt test` |
| `/help` | List all available slash commands |
| `/clear` | Clear conversation context and start fresh |
| `Tab` | Autocomplete file paths in your prompt |

Slash commands are the highest-leverage shortcut — [`/commit`](../../src/claude/skills/commit/SKILL.md), [`/review`](../../src/claude/commands/review.md), and [`/grill_me`](../../src/claude/commands/grill_me.md) invoke multi-step workflows in one word rather than several prompts.
