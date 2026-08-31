# 📊 Claude Usage Report Skill

**Maturity:** Draft (v0.1)  
**Status:** Ready to use for local analysis  

---

## 🎯 Overview

Analyzes your Claude Code usage patterns to validate your default model choice. Generates a self-contained HTML report showing cost efficiency (cost per interaction) and activity intensity (turns per hour) — metrics that reveal whether your model mix is aligned with your workflow patterns.

---

## 💡 Use Case

**When:** You want to understand whether you're using the right model by default.

**Why:** Model choice matters for both cost and latency. Haiku is great for templated workflows (Confluence, Jira, PRs) but costs shouldn't dominate your usage if you're using it efficiently. Opus makes sense for complex reasoning but wastes money if you only use it 2 turns/day.

**Example:** You see $30 charged to Opus but you only use it 20 turns/month on complex problems — justified. But if you see $30/month on Opus for simple templating (high turns/hour on simpler tasks), you should switch to Haiku.

---

## 📋 Scope

**Analyzes:**
- Daily costs by model (Haiku, Sonnet, Opus)
- Turn counts and session counts
- Cost per turn (efficiency: $ ÷ interactions)
- Time span per model per day (first to last timestamp)
- Turns per hour (activity intensity)

**Does not analyze:**
- Prompt content or quality
- External API usage (only Claude Code logs)
- Token cache hit rates (available in raw logs, not in report)
- Relative cost of different use cases (you'd need to tag sessions)

---

## ✨ Capabilities

**What it does:**
- Parses `~/.claude/projects/**/*.jsonl` logs (all project session files)
- Supports flexible date filtering (date ranges, weeks, specific dates)
- Filters by model (Haiku, Sonnet, Opus, or all)
- Calculates interaction metrics (cost/turn, turns/hour, time span)
- Generates self-contained HTML (no external resources, works offline)
- Renders SVG charts for daily costs and model mix trends
- Includes interaction efficiency table showing cost-per-turn by model
- Deduplicates records across multiple log files
- Auto-generates filename based on filters applied

**What it doesn't do:**
- Export to CSV/JSON (report is HTML only; raw data stays in logs)
- Sync with remote analytics
- Delete or modify logs
- Require authentication or API keys
- Access to cost/token data from top-level history.jsonl (metadata only)

---

## 🔐 Security

**Data handling:**
- All analysis is local — no data leaves your machine
- Reads only from `~/.claude/projects/` (your logs)
- Writes only to `~/.claude/_reports/` (generated HTML)
- No credentials, API keys, or secrets involved

**Reversibility:**
- Report is read-only — skill doesn't modify logs
- Generated HTML can be deleted safely
- Logs are not touched

---

## 📋 Prerequisites

- Claude Code installed (logs stored in `~/.claude/projects/`)
- At least one day of usage history to analyze
- Python 3.7+ (stdlib only; no external dependencies)

---

## 🚀 Workflow

### Basic Usage

**Generate default report (last 30 days):**
```bash
/claude_usage_report
# Generates: ~/.claude/_reports/usage_2026-08-21_30d.html
```

**Generate report for specific time period:**
```bash
/claude_usage_report --days 90          # Last 90 days
/claude_usage_report --days 7           # Last 7 days
```

### Advanced Filtering

**Date range (start and end dates):**
```bash
/claude_usage_report --start 2026-08-14 --end 2026-08-20
# Generates: ~/.claude/_reports/usage_2026-08-14-2026-08-20.html
```

**Specific week:**
```bash
/claude_usage_report --week 2026-W34
# Generates: ~/.claude/_reports/usage_2026-W34.html

# Or: week containing a date
/claude_usage_report --week-of 2026-08-19
```

**Filter by model (useful for cost comparisons):**
```bash
/claude_usage_report --days 7 --model haiku
# Haiku-only usage for last 7 days
# Generates: ~/.claude/_reports/usage_2026-08-19-2026-08-21_haiku.html

/claude_usage_report --start 2026-08-14 --end 2026-08-20 --model opus
# Opus-only usage for specific week
```

**Combine filters:**
```bash
# Last week's Haiku usage
/claude_usage_report --week 2026-W34 --model haiku

# Opus only for a date range
/claude_usage_report --start 2026-08-14 --end 2026-08-20 --model opus
```

**Custom output path:**
```bash
/claude_usage_report --days 30 --out ~/Downloads/my_report.html
```

### Interpreting the Report

1. **Summary Cards** (top)
   - Total Cost, Turns, Sessions, Avg Cost per Turn
   - Dominant model and model distribution

2. **Daily Cost Chart**
   - Stacked bar chart by model
   - Identify high-cost days and which models drove them

3. **Model Mix Chart**
   - Line chart showing % of turns by model over time
   - Track shifts in model usage patterns

4. **Interaction Efficiency Table**
   - Cost per turn by model (lower is better)
   - Total cost per model

5. **Daily Metrics Table with Intensity**
   - **Date, Model, Turns:** Activity per model per day
   - **Cost/Turn:** Efficiency metric ($ ÷ interactions)
   - **Time Span (h):** Hours between first and last use
   - **Turns/Hour:** Activity intensity

### Use Cases & Interpretation

**Validating a model switch hypothesis:**
```bash
# Generate reports for comparison
/claude_usage_report --start 2026-08-14 --end 2026-08-20 --model opus   # Last week: expensive
/claude_usage_report --start 2026-08-21 --end 2026-08-27 --model haiku  # This week: cheap

# Compare metrics side-by-side
# - Was cost/turn lower with Haiku?
# - Was turns/hour higher (more active usage)?
```

**Identifying inefficient model usage:**
```bash
/claude_usage_report --days 30 | Look for:
# - High-cost models (Opus/Sonnet) with <1 turn/hour (infrequent use)
# - Cost/turn >> $0.01 (expensive per interaction)
# Solution: Check if you can use Haiku for that use case
```

**Understanding activity patterns:**
```bash
/claude_usage_report --model haiku --days 7 | Look for:
# - Turns/hour > 10 (active, templated workflows)
# - Consistent time span (8+ hours) (sustained usage)
# Insight: Validates using Haiku for sustained, repetitive work
```

---

## 🚨 Error Recovery

**"No log records found in the specified date range"**
- Check: Expand the date range — try `--days 30` or `--days 90`
- Verify: `ls ~/.claude/projects/*/*.jsonl` shows session files
- Note: Only assistant messages with usage data are counted (metadata records are skipped)

**Invalid date format errors**
- Fix: Use YYYY-MM-DD format for all dates
- Examples: `--start 2026-08-19`, `--end 2026-08-21`, `--week-of 2026-08-19`

**Invalid week format**
- Fix: Use YYYY-Www format (ISO 8601 weeks)
- Example: `--week 2026-W34` (week 34 of 2026)

**Model filter returns no results**
- Check: Verify model name is valid (haiku, sonnet, opus)
- Note: Filter is case-insensitive and matches substrings
- Debug: Run without `--model` first to see what models are in the data

**Report shows zero costs**
- Reason: Pricing constants are hardcoded per model
- Check: Ensure records include `message.usage.input_tokens` and `output_tokens`
- Note: Cached tokens (cache_creation_input_tokens, cache_read_input_tokens) are included in input totals

**Log directory not found**
- Check: Claude Code installed and initialized
- Verify: `ls ~/.claude/projects/` shows at least one project directory
- Fix: Run a Claude Code task to create initial log files

---

## 🔗 Related

- `~/.claude/_reference/claude_usage_report_guide.md` — Detailed interpretation guide
- `~/.claude/_tools/claude_usage_report/claude_usage_report.py` — Core parser script

