#!/usr/bin/env python3
"""
Tests for claude_usage_report skill.

Validates:
- Metric calculations (cost per turn, time span, turns per hour)
- Log parsing and aggregation
- HTML report generation and SVG charts
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta, timezone
import sys

# Add tool path to import
sys.path.insert(0, str(Path.home() / ".claude" / "_tools" / "claude_usage_report"))

from claude_usage_report import (
    normalize_model,
    parse_timestamp,
    parse_cli_date,
    parse_cli_week,
    generate_report_filename,
    get_model_css_class,
    parse_logs,
    aggregate_by_day,
    calculate_summary,
    render_html,
)


def create_test_log_record(
    timestamp: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    session_id: str = "test-session-1",
) -> dict:
    """Create a synthetic log record for testing."""
    return {
        "type": "assistant",
        "timestamp": timestamp,
        "sessionId": session_id,
        "message": {
            "model": model,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        },
    }


def test_normalize_model():
    """Validates model name normalization."""
    assert normalize_model("claude-haiku-4-5-20251001") == "claude-haiku-4-5"
    assert normalize_model("claude-sonnet-4-6") == "claude-sonnet-5"
    assert normalize_model("claude-opus-4-6") == "claude-opus-4-8"
    assert normalize_model("haiku") == "claude-haiku-4-5"
    assert normalize_model("sonnet") == "claude-sonnet-5"
    assert normalize_model("opus") == "claude-opus-4-8"
    assert normalize_model("unknown-model") == "unknown"
    assert normalize_model("") == "unknown"
    print("✓ test_normalize_model passed")


def test_cost_per_turn_calculation():
    """Validates cost per turn metric calculation."""
    records = [
        create_test_log_record(
            "2026-08-21T09:00:00Z",
            "claude-haiku-4-5",
            1_000_000,  # 1M input tokens
            200_000,    # 200k output tokens
        ),
        create_test_log_record(
            "2026-08-21T10:00:00Z",
            "claude-haiku-4-5",
            1_000_000,
            200_000,
        ),
    ]

    daily_costs = aggregate_by_day(iter(records))
    assert "2026-08-21" in daily_costs

    haiku_data = daily_costs["2026-08-21"]["claude-haiku-4-5"]
    assert haiku_data["turns"] == 2

    # Cost calculation: input: (2M / 1M) * 1.00 = 2.00, output: (400k / 1M) * 5.00 = 2.00
    expected_total_cost = round(2.00 + 2.00, 4)
    assert haiku_data["cost"] == expected_total_cost

    # Cost per turn: 4.00 / 2 turns = 2.00
    expected_cost_per_turn = round(expected_total_cost / 2, 4)
    assert haiku_data["cost_per_turn"] == expected_cost_per_turn
    print("✓ test_cost_per_turn_calculation passed")


def test_time_span_hours():
    """Validates time span calculation (first to last timestamp)."""
    # Record 1 at 08:00, Record 2 at 16:00 = 8 hour span
    records = [
        create_test_log_record(
            "2026-08-21T08:00:00Z",
            "claude-haiku-4-5",
            100_000,
            20_000,
        ),
        create_test_log_record(
            "2026-08-21T16:00:00Z",
            "claude-haiku-4-5",
            100_000,
            20_000,
        ),
    ]

    daily_costs = aggregate_by_day(iter(records))
    haiku_data = daily_costs["2026-08-21"]["claude-haiku-4-5"]

    assert haiku_data["time_span_hours"] == 8.0
    print("✓ test_time_span_hours passed")


def test_turns_per_hour():
    """Validates turns per hour (activity intensity) calculation."""
    # 4 turns over 2 hours = 2 turns/hour
    records = [
        create_test_log_record(f"2026-08-21T08:00:{i:02d}Z", "claude-haiku-4-5", 100_000, 20_000)
        for i in range(0, 4)  # 4 records at different times
    ]
    # Space them out: 0, 1, 2, 3 seconds → approximately 0 hours span
    # Better test: records at 0, 30, 60, 90 minutes
    records = [
        create_test_log_record(
            "2026-08-21T08:00:00Z",
            "claude-haiku-4-5",
            100_000,
            20_000,
        ),
        create_test_log_record(
            "2026-08-21T08:30:00Z",
            "claude-haiku-4-5",
            100_000,
            20_000,
        ),
        create_test_log_record(
            "2026-08-21T09:00:00Z",
            "claude-haiku-4-5",
            100_000,
            20_000,
        ),
        create_test_log_record(
            "2026-08-21T09:30:00Z",
            "claude-haiku-4-5",
            100_000,
            20_000,
        ),
    ]

    daily_costs = aggregate_by_day(iter(records))
    haiku_data = daily_costs["2026-08-21"]["claude-haiku-4-5"]

    # Time span: 1.5 hours, 4 turns → 2.67 turns/hour
    assert haiku_data["time_span_hours"] == 1.5
    assert haiku_data["turns"] == 4
    assert haiku_data["turns_per_hour"] == round(4 / 1.5, 2)
    print("✓ test_turns_per_hour passed")


def test_summary_calculation():
    """Validates summary statistics including avg cost per turn."""
    records = [
        create_test_log_record("2026-08-21T09:00:00Z", "claude-haiku-4-5", 100_000, 20_000),
        create_test_log_record("2026-08-21T10:00:00Z", "claude-opus-4-8", 100_000, 20_000),
    ]

    daily_costs = aggregate_by_day(iter(records))
    summary = calculate_summary(daily_costs)

    assert summary["total_turns"] == 2
    assert summary["total_cost"] > 0
    assert summary["avg_cost_per_turn"] > 0
    assert "claude-haiku-4-5" in summary["avg_cost_per_turn_by_model"]
    assert "claude-opus-4-8" in summary["avg_cost_per_turn_by_model"]

    # Opus should have higher cost per turn
    assert summary["avg_cost_per_turn_by_model"]["claude-opus-4-8"] > summary["avg_cost_per_turn_by_model"]["claude-haiku-4-5"]
    print("✓ test_summary_calculation passed")


def test_html_report_generation():
    """Validates HTML report is generated and contains expected sections."""
    records = [
        create_test_log_record("2026-08-21T09:00:00Z", "claude-haiku-4-5", 100_000, 20_000),
        create_test_log_record("2026-08-22T09:00:00Z", "claude-sonnet-5", 500_000, 100_000),
    ]

    daily_costs = aggregate_by_day(iter(records))
    summary = calculate_summary(daily_costs)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_report.html"
        render_html(daily_costs, summary, str(output_path))

        assert output_path.exists()
        content = output_path.read_text()

        # Verify key sections
        assert "<html" in content
        assert "Claude Usage Report" in content
        assert "<svg" in content  # SVG charts
        assert "Daily Metrics with Intensity" in content
        assert "Cost/Turn" in content
        assert "Turns/Hour" in content
        assert "claude-haiku-4-5" in content
        assert "claude-sonnet-5" in content

    print("✓ test_html_report_generation passed")


def test_multiple_sessions_per_day():
    """Validates session count aggregation."""
    records = [
        create_test_log_record("2026-08-21T09:00:00Z", "claude-haiku-4-5", 100_000, 20_000, session_id="session-1"),
        create_test_log_record("2026-08-21T10:00:00Z", "claude-haiku-4-5", 100_000, 20_000, session_id="session-2"),
        create_test_log_record("2026-08-21T11:00:00Z", "claude-haiku-4-5", 100_000, 20_000, session_id="session-2"),
    ]

    daily_costs = aggregate_by_day(iter(records))
    assert daily_costs["2026-08-21"]["_sessions"] == 2  # Two unique sessions
    print("✓ test_multiple_sessions_per_day passed")


def test_no_records():
    """Validates handling of empty record set."""
    daily_costs = aggregate_by_day(iter([]))
    summary = calculate_summary(daily_costs)

    assert summary["total_cost"] == 0
    assert summary["total_turns"] == 0
    assert summary["avg_cost_per_turn"] == 0
    print("✓ test_no_records passed")


def test_parse_timestamp_iso_8601():
    """Validates ISO 8601 timestamp parsing."""
    ts_str = "2026-08-21T09:53:51.539Z"
    result = parse_timestamp(ts_str)

    assert result is not None
    assert result.year == 2026
    assert result.month == 8
    assert result.day == 21
    assert result.tzinfo == timezone.utc
    print("✓ test_parse_timestamp_iso_8601 passed")


def test_parse_timestamp_unix_milliseconds():
    """Validates Unix milliseconds timestamp parsing."""
    ts_ms = 1787306400000  # 2026-08-21T10:00:00Z
    result = parse_timestamp(ts_ms)

    assert result is not None
    assert result.year == 2026
    assert result.month == 8
    assert result.day == 21
    assert result.tzinfo == timezone.utc
    print("✓ test_parse_timestamp_unix_milliseconds passed")


def test_parse_timestamp_invalid():
    """Validates that invalid timestamps return None."""
    invalid_cases = [None, "", "invalid", 99999999999999999999]

    for case in invalid_cases:
        result = parse_timestamp(case)
        assert result is None, f"Expected None for {case}, got {result}"

    print("✓ test_parse_timestamp_invalid passed")


def test_parse_cli_date():
    """Validates CLI date parsing."""
    result = parse_cli_date("2026-08-21")

    assert result.year == 2026
    assert result.month == 8
    assert result.day == 21
    assert result.hour == 0
    assert result.minute == 0
    assert result.tzinfo == timezone.utc
    print("✓ test_parse_cli_date passed")


def test_parse_cli_date_invalid():
    """Validates invalid date format handling."""
    invalid_cases = ["2026/08/21", "08-21-2026", "21st August 2026"]

    for case in invalid_cases:
        try:
            parse_cli_date(case)
            assert False, f"Expected ValueError for {case}"
        except ValueError:
            pass

    print("✓ test_parse_cli_date_invalid passed")


def test_parse_cli_week():
    """Validates ISO week parsing."""
    # Week 34 of 2026 should be Aug 17-23
    start_date, end_date = parse_cli_week("2026-W34")

    assert start_date.year == 2026
    assert start_date.month == 8
    assert start_date.day == 17  # Monday of week 34
    assert start_date.weekday() == 0  # Monday

    assert end_date.year == 2026
    assert end_date.month == 8
    assert end_date.day == 23  # Sunday of week 34
    assert end_date.weekday() == 6  # Sunday

    # 7-day span
    assert (end_date - start_date).days == 6

    print("✓ test_parse_cli_week passed")


def test_parse_cli_week_invalid():
    """Validates invalid week format handling."""
    invalid_cases = ["2026-34", "W34-2026", "invalid"]

    for case in invalid_cases:
        try:
            parse_cli_week(case)
            assert False, f"Expected ValueError for {case}"
        except ValueError:
            pass

    print("✓ test_parse_cli_week_invalid passed")


def test_generate_report_filename_date_range():
    """Validates report filename generation with date range."""
    start = datetime(2026, 8, 19, tzinfo=timezone.utc)
    end = datetime(2026, 8, 20, tzinfo=timezone.utc)

    filename = generate_report_filename(start, end, None)
    assert "usage_2026-08-19-2026-08-20.html" in filename
    print("✓ test_generate_report_filename_date_range passed")


def test_generate_report_filename_with_model():
    """Validates report filename generation with model filter."""
    start = datetime(2026, 8, 19, tzinfo=timezone.utc)
    end = datetime(2026, 8, 20, tzinfo=timezone.utc)

    filename = generate_report_filename(start, end, "haiku")
    assert "haiku.html" in filename
    assert "2026-08-19-2026-08-20" in filename
    print("✓ test_generate_report_filename_with_model passed")


def test_generate_report_filename_week():
    """Validates report filename generation for week-based ranges."""
    # Week 34 (Aug 17-23, 2026)
    start = datetime(2026, 8, 17, tzinfo=timezone.utc)
    end = datetime(2026, 8, 23, tzinfo=timezone.utc)

    filename = generate_report_filename(start, end, None)
    assert "usage_2026-W34.html" in filename
    print("✓ test_generate_report_filename_week passed")


def test_get_model_css_class():
    """Validates CSS class extraction from model names."""
    cases = [
        ("claude-haiku-4-5", "haiku"),
        ("claude-sonnet-5", "sonnet"),
        ("claude-opus-4-8", "opus"),
        ("unknown-model", "unknown"),
    ]

    for model, expected_class in cases:
        result = get_model_css_class(model)
        assert result == expected_class, f"get_model_css_class({model}) = {result}, expected {expected_class}"

    print("✓ test_get_model_css_class passed")


if __name__ == "__main__":
    # Existing tests
    test_normalize_model()
    test_cost_per_turn_calculation()
    test_time_span_hours()
    test_turns_per_hour()
    test_summary_calculation()
    test_html_report_generation()
    test_multiple_sessions_per_day()
    test_no_records()

    # New tests for Phase 2
    test_parse_timestamp_iso_8601()
    test_parse_timestamp_unix_milliseconds()
    test_parse_timestamp_invalid()
    test_parse_cli_date()
    test_parse_cli_date_invalid()
    test_parse_cli_week()
    test_parse_cli_week_invalid()
    test_generate_report_filename_date_range()
    test_generate_report_filename_with_model()
    test_generate_report_filename_week()
    test_get_model_css_class()

    print("\n✅ All tests passed (18 tests)")
