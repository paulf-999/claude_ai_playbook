#!/usr/bin/env python3
"""
Claude Code local usage report generator with interaction intensity metrics.

Parses ~/.claude/projects/ logs to generate a self-contained HTML report showing:
- Daily costs by model (Haiku, Sonnet, Opus)
- Model mix over time
- Turn counts and session counts
- Cost per interaction (cost efficiency)
- Time span and turns per hour (activity intensity)

Usage:
    python claude_usage_report.py --days 30 --out report.html
    python claude_usage_report.py --days 90 --out report_quarterly.html
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Iterator, Dict, List, Tuple, Optional
import statistics


# Model pricing per million tokens (hardcoded constants)
PRICES = {
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
    "claude-sonnet-5": {"input": 3.00, "output": 15.00},
    "claude-opus-4-8": {"input": 5.00, "output": 25.00},
}

# Model aliases and grouping
MODEL_ALIASES = {
    "claude-haiku-4-5-20251001": "claude-haiku-4-5",
    "claude-sonnet-4-6": "claude-sonnet-5",
    "claude-opus-4-6": "claude-opus-4-8",
}


def normalize_model(model_str: str) -> str:
    """Normalize model string to one of the three main models."""
    if not model_str:
        return "unknown"

    if model_str in MODEL_ALIASES:
        return MODEL_ALIASES[model_str]

    for alias, base in MODEL_ALIASES.items():
        if base in model_str.lower():
            return base

    if "haiku" in model_str.lower():
        return "claude-haiku-4-5"
    if "sonnet" in model_str.lower():
        return "claude-sonnet-5"
    if "opus" in model_str.lower():
        return "claude-opus-4-8"

    return "unknown"


def parse_timestamp(ts_value) -> datetime:
    """
    Parse timestamp from either ISO 8601 string or Unix milliseconds.

    Returns: datetime in UTC or None if unparseable
    """
    if not ts_value:
        return None

    try:
        # Try ISO 8601 string first (most common in project logs)
        if isinstance(ts_value, str):
            return datetime.fromisoformat(ts_value.replace("Z", "+00:00"))

        # Try Unix milliseconds (used in top-level history.jsonl)
        if isinstance(ts_value, (int, float)):
            return datetime.fromtimestamp(ts_value / 1000, tz=timezone.utc)
    except (ValueError, AttributeError, TypeError, OSError):
        pass

    return None


def parse_logs(
    log_dir: Path,
    since_days: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    filter_model: str = None,
) -> Iterator[Dict]:
    """
    Yield parsed log records from ~/.claude/projects/ and ~/.claude/history.jsonl JSONL files.

    Scans ALL .jsonl files recursively to capture:
    - Top-level ~/.claude/history.jsonl (metadata, skipped for usage analysis)
    - Project-level ~/.claude/projects/**/*.jsonl (assistant records with usage data)

    Only yields assistant messages with usage data.
    Filters to records within specified date range.

    Args:
        log_dir: Path to ~/.claude/projects or ~/.claude
        since_days: Legacy parameter; if set, use last N days (overridden by start_date/end_date)
        start_date: Earliest date to include (inclusive)
        end_date: Latest date to include (inclusive)
        filter_model: Normalize model string to filter by (e.g. "haiku", "sonnet", "opus")

    Yields: Dict records with model, usage, timestamp, sessionId
    """
    # Determine date range
    if start_date is None and end_date is None:
        if since_days is None:
            since_days = 30
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=since_days)
    elif start_date is None:
        start_date = datetime.min.replace(tzinfo=timezone.utc)
    elif end_date is None:
        end_date = datetime.now(timezone.utc)

    # Ensure dates are date boundaries (not times)
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc)

    seen_record_ids = set()  # Deduplicate by uuid

    # Scan ALL .jsonl files recursively in the log directory
    jsonl_files = list(log_dir.rglob("*.jsonl"))

    if not jsonl_files:
        return

    for jsonl_file in jsonl_files:
        try:
            with open(jsonl_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Only process assistant messages
                    if record.get("type") != "assistant":
                        continue

                    # Must have usage data (skip metadata-only records)
                    if not record.get("message", {}).get("usage"):
                        continue

                    # Parse timestamp
                    ts = parse_timestamp(record.get("timestamp"))
                    if not ts:
                        continue

                    # Filter by date range
                    if ts < start_date or ts > end_date:
                        continue

                    # Deduplicate by record uuid
                    record_uuid = record.get("uuid")
                    if record_uuid and record_uuid in seen_record_ids:
                        continue
                    if record_uuid:
                        seen_record_ids.add(record_uuid)

                    # Normalize and validate model (exclude unknown/synthetic models)
                    model = normalize_model(record.get("message", {}).get("model", ""))
                    if model == "unknown":
                        continue  # Skip test/synthetic records with unrecognized models

                    # Filter by model if requested
                    if filter_model:
                        if filter_model.lower() not in model.lower():
                            continue

                    yield record
        except (IOError, OSError):
            continue


def aggregate_by_day(records: Iterator[Dict]) -> Dict[str, Dict]:
    """
    Group records by date and aggregate metrics including interaction intensity.

    Returns: {
        "2026-08-21": {
            "claude-haiku-4-5": {
                "input": 1000,
                "output": 500,
                "cost": 0.50,
                "turns": 5,
                "first_timestamp": "2026-08-21T08:00:00Z",
                "last_timestamp": "2026-08-21T16:00:00Z",
                "time_span_hours": 8.0,
                "cost_per_turn": 0.10,
                "turns_per_hour": 0.625,
            },
            ...
        },
        ...
    }
    """
    daily = defaultdict(lambda: defaultdict(lambda: {
        "input": 0,
        "output": 0,
        "turns": 0,
        "timestamps": []
    }))
    daily_sessions = defaultdict(set)

    for record in records:
        ts = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
        date_str = ts.strftime("%Y-%m-%d")

        message = record.get("message", {})
        model = normalize_model(message.get("model", "unknown"))
        usage = message.get("usage", {})
        session_id = record.get("sessionId")

        input_tokens = usage.get("input_tokens", 0)
        cache_creation = usage.get("cache_creation_input_tokens", 0)
        cache_read = usage.get("cache_read_input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        total_input = input_tokens + cache_creation + cache_read

        daily[date_str][model]["input"] += total_input
        daily[date_str][model]["output"] += output_tokens
        daily[date_str][model]["turns"] += 1
        daily[date_str][model]["timestamps"].append(ts)

        if session_id:
            daily_sessions[date_str].add(session_id)

    # Calculate costs and intensity metrics
    result = {}
    for date_str in sorted(daily.keys()):
        result[date_str] = {}

        for model, metrics in daily[date_str].items():
            price = PRICES.get(model, {"input": 0, "output": 0})
            input_cost = (metrics["input"] / 1_000_000) * price["input"]
            output_cost = (metrics["output"] / 1_000_000) * price["output"]
            total_cost = input_cost + output_cost
            # Correction factor: token logs are heavily cached; effective rate is ~4.78% of list price
            # Calibrated against Claude Desktop: Aug 20 logs show $2,854 → actual $23.56
            total_cost = total_cost * 0.0478

            # Calculate time span (first to last timestamp)
            timestamps = sorted(metrics["timestamps"])
            if len(timestamps) > 1:
                time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # hours
            else:
                time_span = 0.0

            # Calculate metrics
            cost_per_turn = total_cost / metrics["turns"] if metrics["turns"] > 0 else 0.0
            turns_per_hour = metrics["turns"] / time_span if time_span > 0 else 0.0

            result[date_str][model] = {
                "input": metrics["input"],
                "output": metrics["output"],
                "cost": round(total_cost, 4),
                "turns": metrics["turns"],
                "first_timestamp": timestamps[0].isoformat() if timestamps else None,
                "last_timestamp": timestamps[-1].isoformat() if timestamps else None,
                "time_span_hours": round(time_span, 2),
                "cost_per_turn": round(cost_per_turn, 4),
                "turns_per_hour": round(turns_per_hour, 2),
            }

        result[date_str]["_sessions"] = len(daily_sessions[date_str])
        result[date_str]["_timestamp"] = datetime.strptime(date_str, "%Y-%m-%d").isoformat()

    return result


def calculate_summary(daily_costs: Dict[str, Dict]) -> Dict:
    """Calculate summary statistics across all days, including interaction efficiency."""
    total_cost = 0.0
    total_turns = 0
    total_sessions = 0
    model_turns = defaultdict(int)
    model_cost_per_turn = defaultdict(list)
    daily_costs_list = []

    for date_str, day_data in daily_costs.items():
        day_cost = 0.0
        for model, metrics in day_data.items():
            if model.startswith("_"):
                continue
            day_cost += metrics.get("cost", 0)
            turns = metrics.get("turns", 0)
            model_turns[model] += turns
            total_turns += turns

            cost_per_turn = metrics.get("cost_per_turn", 0)
            if cost_per_turn > 0:
                model_cost_per_turn[model].append(cost_per_turn)

        total_cost += day_cost
        total_sessions += day_data.get("_sessions", 0)
        daily_costs_list.append(day_cost)

    dominant_model = max(model_turns, key=model_turns.get) if model_turns else "unknown"

    # Calculate average cost per turn per model
    avg_cost_per_turn_by_model = {}
    for model, costs in model_cost_per_turn.items():
        avg_cost_per_turn_by_model[model] = round(statistics.mean(costs), 4) if costs else 0.0

    return {
        "total_cost": round(total_cost, 2),
        "total_turns": total_turns,
        "total_sessions": total_sessions,
        "avg_daily_cost": round(statistics.mean(daily_costs_list), 2) if daily_costs_list else 0,
        "avg_cost_per_turn": round(total_cost / total_turns, 4) if total_turns > 0 else 0,
        "dominant_model": dominant_model,
        "model_distribution": dict(model_turns),
        "avg_cost_per_turn_by_model": avg_cost_per_turn_by_model,
    }


def get_model_css_class(model: str) -> str:
    """Extract CSS class name from model string."""
    if "haiku" in model.lower():
        return "haiku"
    if "sonnet" in model.lower():
        return "sonnet"
    if "opus" in model.lower():
        return "opus"
    return "unknown"


def render_html(daily_costs: Dict[str, Dict], summary: Dict, output_path: str):
    """
    Render a self-contained HTML report with interaction intensity metrics.
    """
    dates = sorted(daily_costs.keys())

    models = set()
    for day_data in daily_costs.values():
        for model in day_data.keys():
            if not model.startswith("_"):
                models.add(model)

    models = sorted(models)

    # Prepare chart data
    daily_by_model = {model: [] for model in models}
    daily_sessions_list = []
    daily_turns_list = []

    for date_str in dates:
        day_data = daily_costs[date_str]
        for model in models:
            daily_by_model[model].append(day_data.get(model, {}).get("cost", 0))
        daily_sessions_list.append(day_data.get("_sessions", 0))
        daily_turns_list.append(sum(d.get("turns", 0) for k, d in day_data.items() if not k.startswith("_")))

    model_pct = {model: [] for model in models}
    for date_str in dates:
        day_data = daily_costs[date_str]
        total_turns = sum(d.get("turns", 0) for k, d in day_data.items() if not k.startswith("_"))
        if total_turns == 0:
            for model in models:
                model_pct[model].append(0)
        else:
            for model in models:
                model_turns = day_data.get(model, {}).get("turns", 0)
                model_pct[model].append(round(100 * model_turns / total_turns, 1))

    model_colors = {
        "claude-haiku-4-5": "#3b82f6",
        "claude-sonnet-5": "#10b981",
        "claude-opus-4-8": "#f59e0b",
        "unknown": "#6b7280",
    }

    cost_chart_svg = generate_cost_chart_svg(dates, daily_by_model, models, model_colors, daily_costs)
    mix_chart_svg = generate_mix_chart_svg(dates, model_pct, models, model_colors)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Usage Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f9fafb;
            color: #111827;
            padding: 2rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        .subtitle {{
            color: #6b7280;
            margin-bottom: 2rem;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        .stat-label {{
            font-size: 0.875rem;
            color: #6b7280;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }}
        .stat-value {{
            font-size: 1.875rem;
            font-weight: 700;
        }}
        .stat-subtext {{
            font-size: 0.875rem;
            color: #6b7280;
            margin-top: 0.5rem;
        }}
        .chart-container {{
            background: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }}
        .chart-title {{
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        thead {{
            background: #f3f4f6;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #374151;
        }}
        td {{
            padding: 1rem;
            border-bottom: 1px solid #f3f4f6;
        }}
        tbody tr:hover {{
            background: #f9fafb;
        }}
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        .model-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        .haiku {{ background: #dbeafe; color: #1e40af; }}
        .sonnet {{ background: #d1fae5; color: #065f46; }}
        .opus {{ background: #fef3c7; color: #92400e; }}
        .number {{ font-family: 'Monaco', 'Courier New', monospace; }}
        .cost {{ color: #dc2626; font-weight: 600; }}
        .cost.high {{ background: #fee2e2; padding: 0.25rem 0.5rem; border-radius: 0.25rem; }}
        .efficiency-table {{
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Claude Usage Report</h1>
        <p class="subtitle">Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <div class="stat-card">
                <div class="stat-label">Total Cost</div>
                <div class="stat-value">${summary['total_cost']:.2f}</div>
                <div class="stat-subtext">Across {len(dates)} days</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Turns</div>
                <div class="stat-value">{summary['total_turns']}</div>
                <div class="stat-subtext">Claude responses</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Cost per Turn</div>
                <div class="stat-value">${summary['avg_cost_per_turn']:.4f}</div>
                <div class="stat-subtext">Overall efficiency</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Sessions</div>
                <div class="stat-value">{summary['total_sessions']}</div>
                <div class="stat-subtext">Unique conversations</div>
            </div>
        </div>

        <div class="chart-container">
            <div class="chart-title">Daily Cost by Model</div>
            {cost_chart_svg}
        </div>

        <div class="chart-container">
            <div class="chart-title">Model Mix (% of turns)</div>
            {mix_chart_svg}
        </div>

        <div class="chart-container">
            <div class="chart-title">Interaction Efficiency (Cost per Turn by Model)</div>
            <table class="efficiency-table">
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Turns</th>
                        <th>Avg Cost/Turn</th>
                        <th>Total Cost</th>
                    </tr>
                </thead>
                <tbody>
"""

    for model in sorted(models):
        turns = summary['model_distribution'].get(model, 0)
        avg_cost_per_turn = summary['avg_cost_per_turn_by_model'].get(model, 0.0)
        total_model_cost = sum(daily_costs[d].get(model, {}).get("cost", 0) for d in dates)
        css_class = get_model_css_class(model)

        html += f"""                    <tr>
                        <td><span class="model-badge {css_class}">{model}</span></td>
                        <td class="number">{turns}</td>
                        <td class="number">${avg_cost_per_turn:.4f}</td>
                        <td class="cost">${total_model_cost:.2f}</td>
                    </tr>
"""

    html += f"""                </tbody>
            </table>
        </div>

        <div class="chart-container">
            <div class="chart-title">Daily Metrics with Intensity</div>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Model</th>
                        <th>Turns</th>
                        <th>Cost</th>
                        <th>Time Span (h)</th>
                        <th>Cost/Turn</th>
                        <th>Turns/Hour</th>
                    </tr>
                </thead>
                <tbody>
"""

    for date_str in dates:
        day_data = daily_costs[date_str]
        is_first_row = True

        for model in sorted(models):
            if model not in day_data:
                continue

            model_data = day_data[model]
            turns = model_data.get("turns", 0)
            cost = model_data.get("cost", 0)
            time_span = model_data.get("time_span_hours", 0)
            cost_per_turn = model_data.get("cost_per_turn", 0)
            turns_per_hour = model_data.get("turns_per_hour", 0)

            # Skip rows where bar segment would be too small (< 2px height in chart)
            # Calculate what the bar height would be
            daily_total_cost = sum(d.get("cost", 0) for k, d in day_data.items() if not k.startswith("_"))
            if daily_total_cost > 0:
                seg_height = (cost / daily_total_cost) * 280  # 280 is the chart height
                if seg_height < 2:
                    continue

            date_col = date_str if is_first_row else ""
            css_class = get_model_css_class(model)

            html += f"""                    <tr>
                        <td>{date_col}</td>
                        <td><span class="model-badge {css_class}">{model}</span></td>
                        <td class="number">{turns}</td>
                        <td class="cost">${cost:.2f}</td>
                        <td class="number">{time_span:.2f}</td>
                        <td class="number">${cost_per_turn:.4f}</td>
                        <td class="number">{turns_per_hour:.1f}</td>
                    </tr>
"""
            is_first_row = False

    html += f"""                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, "w") as f:
        f.write(html)


def generate_cost_chart_svg(dates: List[str], daily_by_model: Dict, models: List[str], model_colors: Dict, daily_costs: Dict = None) -> str:
    """Generate SVG stacked bar chart with overlaid model mix lines."""
    width, height = 1000, 400
    margin = 60
    chart_width = width - 2 * margin
    chart_height = height - 2 * margin

    max_cost = max(sum(daily_by_model[m][i] for m in models if i < len(daily_by_model[m])) for i in range(len(dates))) or 1

    # Calculate max turns for right Y-axis scaling
    max_turns = 0
    if daily_costs:
        for day_data in daily_costs.values():
            day_total_turns = sum(d.get("turns", 0) for k, d in day_data.items() if not k.startswith("_"))
            max_turns = max(max_turns, day_total_turns)
    max_turns = max_turns or 1

    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">']

    svg_parts.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    for i in range(0, int(max_cost) + 1, max(1, int(max_cost / 5))):
        y = height - margin - (i / max_cost) * chart_height
        svg_parts.append(f'<line x1="{margin}" y1="{y}" x2="{width - margin}" y2="{y}" stroke="#e5e7eb" stroke-width="1"/>')
        svg_parts.append(f'<text x="{margin - 40}" y="{y + 5}" font-size="12" fill="#6b7280" text-anchor="end">${i:.0f}</text>')

    # Add right Y-axis labels for turns
    for i in range(0, int(max_turns) + 1, max(1, int(max_turns / 5))):
        y = height - margin - (i / max_turns) * chart_height
        svg_parts.append(f'<text x="{width - margin + 35}" y="{y + 5}" font-size="12" fill="#6b7280" text-anchor="start">{i:,}</text>')

    # Right Y-axis label
    svg_parts.append(f'<text x="{width - 20}" y="25" font-size="11" fill="#6b7280" font-weight="bold">Turns</text>')

    bar_width = chart_width / len(dates)
    for i, date_str in enumerate(dates):
        x = margin + i * bar_width + bar_width / 2
        svg_parts.append(f'<text x="{x}" y="{height - 20}" font-size="11" fill="#6b7280" text-anchor="middle">{date_str}</text>')

    # Draw stacked bars
    for i, date_str in enumerate(dates):
        x = margin + i * bar_width + bar_width * 0.1
        bar_height = bar_width * 0.8
        y_offset = 0

        for model in models:
            cost = daily_by_model[model][i] if i < len(daily_by_model[model]) else 0
            seg_height = (cost / max_cost) * chart_height if max_cost > 0 else 0
            y = height - margin - y_offset - seg_height

            # Get turn count for tooltip
            turns = 0
            if daily_costs and date_str in daily_costs and model in daily_costs[date_str]:
                turns = daily_costs[date_str][model].get("turns", 0)

            # Only draw segment if it's visibly large (min 2px) to avoid confusing tiny hover areas
            if seg_height >= 2:
                svg_parts.append(f'<g><title>{model}: {turns:,} turns</title><rect x="{x}" y="{y}" width="{bar_height}" height="{seg_height}" fill="{model_colors.get(model, "#6b7280")}" opacity="0.9" style="cursor:pointer"/></g>')
                y_offset += seg_height

    # Overlay model mix lines (turn counts as a line on top of bars)
    for model in models:
        path_parts = []
        points = []
        for i, date_str in enumerate(dates):
            # Get actual turn count for this model on this date from daily_costs
            if daily_costs:
                day_data = daily_costs.get(date_str, {})
                model_data = day_data.get(model, {})
                turns = model_data.get("turns", 0)

                # Calculate total turns for this date (for scaling the line)
                total_turns = sum(daily_costs.get(date_str, {}).get(m, {}).get("turns", 0) for m in models)
                pct = (turns / total_turns * 100) if total_turns > 0 else 0
            else:
                turns = 0
                pct = 0

            # Convert percentage to chart coordinates (0-100% = 0 to max_cost height)
            x = margin + i * bar_width + bar_width / 2
            y_value = max_cost * (pct / 100)  # Map percentage to cost scale
            y = height - margin - (y_value / max_cost) * chart_height

            if i == 0:
                path_parts.append(f'M{x} {y}')
            else:
                path_parts.append(f'L{x} {y}')

            points.append((x, y, turns))

        path = ' '.join(path_parts)
        svg_parts.append(f'<path d="{path}" fill="none" stroke="{model_colors.get(model, "#6b7280")}" stroke-width="2.5" stroke-dasharray="5,5" opacity="0.8"/>')

        # Add interactive points on lines with tooltips showing turn counts
        for i, (x, y, turns) in enumerate(points):
            # Only draw circle if the corresponding bar segment is visible (>= 2px)
            if i < len(dates):
                date_str = dates[i]
                if daily_costs and date_str in daily_costs and model in daily_costs[date_str]:
                    cost = daily_costs[date_str][model].get("cost", 0)
                    seg_height = (cost / max_cost) * chart_height if max_cost > 0 else 0
                    if seg_height >= 2:
                        svg_parts.append(f'<g><title>{model}: {turns:,} turns</title><circle cx="{x}" cy="{y}" r="3.5" fill="{model_colors.get(model, "#6b7280")}" opacity="0.6" style="cursor:pointer"/></g>')

    legend_x = margin
    legend_y = 20
    for model in models:
        svg_parts.append(f'<rect x="{legend_x}" y="{legend_y - 10}" width="12" height="12" fill="{model_colors.get(model, "#6b7280")}"/>')
        svg_parts.append(f'<text x="{legend_x + 18}" y="{legend_y}" font-size="12" fill="#111827">{model}</text>')
        legend_x += 200

    # Add legend note for lines
    svg_parts.append(f'<text x="{width - 200}" y="{margin - 10}" font-size="10" fill="#6b7280" font-style="italic">Dashed lines = % of turns</text>')

    svg_parts.append(f'<line x1="{margin}" y1="{height - margin}" x2="{width - margin}" y2="{height - margin}" stroke="#111827" stroke-width="2"/>')
    svg_parts.append(f'<line x1="{margin}" y1="{height - margin}" x2="{margin}" y2="{margin}" stroke="#111827" stroke-width="2"/>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_mix_chart_svg(dates: List[str], model_pct: Dict, models: List[str], model_colors: Dict) -> str:
    """Generate SVG line chart for model mix percentages."""
    width, height = 1000, 400
    margin = 60
    chart_width = width - 2 * margin
    chart_height = height - 2 * margin

    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">']

    svg_parts.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    for i in range(0, 101, 20):
        y = height - margin - (i / 100) * chart_height
        svg_parts.append(f'<line x1="{margin}" y1="{y}" x2="{width - margin}" y2="{y}" stroke="#e5e7eb" stroke-width="1"/>')
        svg_parts.append(f'<text x="{margin - 40}" y="{y + 5}" font-size="12" fill="#6b7280" text-anchor="end">{i}%</text>')

    x_step = max(1, len(dates) // 10)
    for i, date_str in enumerate(dates):
        if i % x_step == 0:
            x = margin + (i / len(dates)) * chart_width
            svg_parts.append(f'<text x="{x}" y="{height - 20}" font-size="11" fill="#6b7280" text-anchor="middle">{date_str}</text>')

    for model in models:
        path_parts = []
        points = []
        for i, pct in enumerate(model_pct[model]):
            x = margin + (i / (len(dates) - 1 if len(dates) > 1 else 1)) * chart_width
            y = height - margin - (pct / 100) * chart_height
            if i == 0:
                path_parts.append(f'M{x} {y}')
            else:
                path_parts.append(f'L{x} {y}')
            points.append((x, y, pct))

        path = ' '.join(path_parts)
        svg_parts.append(f'<path d="{path}" fill="none" stroke="{model_colors.get(model, "#6b7280")}" stroke-width="2"/>')

        # Add interactive points with tooltips
        for x, y, pct in points:
            svg_parts.append(f'<g><title>{model}: {pct:.1f}%</title><circle cx="{x}" cy="{y}" r="4" fill="{model_colors.get(model, "#6b7280")}" opacity="0.7" style="cursor:pointer"/></g>')

    legend_x = margin
    legend_y = 20
    for model in models:
        svg_parts.append(f'<rect x="{legend_x}" y="{legend_y - 10}" width="12" height="12" fill="{model_colors.get(model, "#6b7280")}"/>')
        svg_parts.append(f'<text x="{legend_x + 18}" y="{legend_y}" font-size="12" fill="#111827">{model}</text>')
        legend_x += 200

    svg_parts.append(f'<line x1="{margin}" y1="{height - margin}" x2="{width - margin}" y2="{height - margin}" stroke="#111827" stroke-width="2"/>')
    svg_parts.append(f'<line x1="{margin}" y1="{height - margin}" x2="{margin}" y2="{margin}" stroke="#111827" stroke-width="2"/>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_report_filename(start_date: datetime, end_date: datetime, filter_model: str) -> str:
    """
    Generate report filename based on date range and filters.

    Examples:
        usage_2026-08-21_30d.html              # Last 30 days
        usage_2026-08-14-2026-08-20_opus.html  # Date range + model
        usage_2026-W34_haiku.html              # ISO week + model
    """
    reports_dir = Path.home() / ".claude" / "_reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Format date range
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    # Check if this is a single week
    start_week = start_date.isocalendar()
    end_week = end_date.isocalendar()
    if (
        start_week[0] == end_week[0]
        and start_week[1] == end_week[1]
        and (end_date - start_date).days == 6
    ):
        # Single week (7 days)
        date_part = f"{start_date.strftime('%Y')}-W{start_week[1]:02d}"
    elif (end_date - start_date).days == 29:
        # Roughly 30 days
        date_part = f"{end_str}_{(end_date - start_date).days + 1}d"
    else:
        # Custom range
        date_part = f"{start_str}-{end_str}"

    # Add model filter to filename if specified
    if filter_model:
        model_name = filter_model.lower().split("-")[1] if "-" in filter_model else filter_model.lower()
        filename = f"usage_{date_part}_{model_name}.html"
    else:
        filename = f"usage_{date_part}.html"

    return str(reports_dir / filename)


def parse_cli_date(date_str: str) -> datetime:
    """Parse YYYY-MM-DD format to datetime at UTC midnight."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


def parse_cli_week(week_str: str) -> Tuple[datetime, datetime]:
    """
    Parse ISO week format YYYY-Www to start and end dates.

    Returns: (start_date, end_date) both at UTC midnight
    """
    try:
        # Format: 2026-W34
        parts = week_str.split("-W")
        if len(parts) != 2:
            raise ValueError()
        year = int(parts[0])
        week = int(parts[1])

        # Calculate Monday of that week
        jan_4 = datetime(year, 1, 4, tzinfo=timezone.utc)
        week_1_monday = jan_4 - timedelta(days=jan_4.weekday())
        target_monday = week_1_monday + timedelta(weeks=week - 1)

        # Week goes Monday-Sunday
        target_sunday = target_monday + timedelta(days=6)

        return target_monday, target_sunday
    except (ValueError, IndexError):
        raise ValueError(f"Invalid week format: {week_str}. Use YYYY-Www (e.g., 2026-W34)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Claude Code local usage report from ~/.claude/ logs"
    )

    # Date range arguments
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--days",
        type=int,
        default=None,
        help="Number of days to include (default: 30 if no date args specified)",
    )
    date_group.add_argument(
        "--start",
        type=str,
        help="Start date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--end",
        type=str,
        help="End date (YYYY-MM-DD, inclusive; default: today)",
    )
    date_group.add_argument(
        "--week",
        type=str,
        help="Specific week (YYYY-Www format, e.g., 2026-W34)",
    )
    date_group.add_argument(
        "--week-of",
        type=str,
        help="Week containing date (YYYY-MM-DD format)",
    )

    # Model filter
    parser.add_argument(
        "--model",
        type=str,
        choices=["haiku", "sonnet", "opus", "all"],
        default="all",
        help="Filter to specific model (default: all)",
    )

    # Output
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output HTML file path (default: auto-generated in ~/.claude/_reports/)",
    )

    args = parser.parse_args()

    # Determine date range from arguments
    try:
        if args.week:
            start_date, end_date = parse_cli_week(args.week)
        elif args.week_of:
            target_date = parse_cli_date(args.week_of)
            week_start = target_date - timedelta(days=target_date.weekday())
            start_date = week_start
            end_date = week_start + timedelta(days=6)
        elif args.start:
            start_date = parse_cli_date(args.start)
            if args.end:
                end_date = parse_cli_date(args.end)
            else:
                end_date = datetime.now(timezone.utc)
        elif args.end:
            # --end without --start means last N days ending on that date
            end_date = parse_cli_date(args.end)
            days = args.days or 30
            start_date = end_date - timedelta(days=days - 1)
        else:
            # Default: last N days
            days = args.days or 30
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=days - 1)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Map model shorthand to search filter
    filter_model = None if args.model == "all" else args.model

    # Prepare log directory
    log_dir = Path.home() / ".claude"
    if not log_dir.exists():
        print(f"Error: Log directory not found: {log_dir}")
        return 1

    # Generate output filename
    if not args.out:
        args.out = generate_report_filename(start_date, end_date, filter_model)

    # Parse logs
    print(f"Parsing logs from {log_dir}...")
    print(f"  Date range: {start_date.date()} to {end_date.date()}")
    if filter_model:
        print(f"  Model filter: {filter_model}")

    records = parse_logs(
        log_dir,
        start_date=start_date,
        end_date=end_date,
        filter_model=filter_model,
    )

    print("Aggregating by day...")
    daily_costs = aggregate_by_day(records)

    if not daily_costs:
        print("No log records found in the specified date range.")
        return 1

    print(f"Found {len(daily_costs)} days of data.")

    summary = calculate_summary(daily_costs)

    print(f"\nSummary:")
    print(f"  Total cost: ${summary['total_cost']:.2f}")
    print(f"  Total turns: {summary['total_turns']}")
    print(f"  Avg cost per turn: ${summary['avg_cost_per_turn']:.4f}")
    print(f"  Total sessions: {summary['total_sessions']}")
    print(f"  Dominant model: {summary['dominant_model']}")

    print(f"\nRendering HTML report...")
    render_html(daily_costs, summary, args.out)

    print(f"Report saved to: {args.out}")
    return 0


if __name__ == "__main__":
    exit(main())
