#!/usr/bin/env python3
# ruff: noqa: F401, F841  # illustrative example; some imports/vars are intentionally unused
"""
Example: Testing patterns from testing/*.md

Demonstrates:
- Test naming: test_<function>_<scenario>
- Test structure: Setup → Execute → Assert
- Pytest fixtures: monkeypatch, tmp_path
- Custom helpers: _make_client(), _entry()
- Mocking: MagicMock, mock assertions
- Exception testing: pytest.raises
"""

import pytest
from unittest.mock import MagicMock

# Assume these are being tested
from config_loader import load_config, validate_config
from airbyte_client import AirbytClient


# ✅ CUSTOM FIXTURE HELPERS (underscore prefix)

def _make_client():
    """Create mock Airbyte client with default return values."""
    client = MagicMock()
    client.base_url = "https://test-server.prod.payroc.com:8006"
    client.list_sources.return_value = []
    client.list_destinations.return_value = []
    client.list_connections.return_value = []
    client.create_source.return_value = {"sourceId": "s1"}
    client.create_destination.return_value = {"destinationId": "d1"}
    return client


def _entry(source_system="salesforce_prod", source_server="dc1_source_1"):
    """Create a sample connection entry for testing."""
    return {
        "source_server": source_server,
        "source_system": source_system,
        "source": {
            "name": "Salesforce Prod",
            "connector_type": "source-salesforce",
            "config": {},
        },
        "destination": {
            "name": "Snowflake Raw",
            "connector_type": "destination-snowflake",
            "config": {},
        },
        "connections": [
            {
                "name": f"{source_system}_conn",
                "schedule": {"type": "manual"},
                "streams": [],
            }
        ],
    }


# ✅ TEST NAMING & STRUCTURE: test_<function>_<scenario>

def test_load_config_reads_yaml_file(tmp_path):
    """When given a valid YAML file, load_config parses and returns config."""
    # Setup: Create a temp YAML file
    config_path = tmp_path / "config.yaml"
    config_path.write_text("source: salesforce\nconnections: []")

    # Execute: Call the function
    result = load_config(str(config_path))

    # Assert: Verify expected behaviour
    assert result["source"] == "salesforce"
    assert "connections" in result


def test_load_config_raises_on_file_not_found():
    """When file doesn't exist, FileNotFoundError is raised."""
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/path.yaml")


def test_validate_config_raises_on_invalid_table_descriptor():
    """When table_descriptor is invalid, ValueError is raised with descriptive message."""
    invalid_config = {
        "connections": [{"table_descriptor": "invalid_descriptor"}]
    }
    with pytest.raises(ValueError, match="Invalid table_descriptor"):
        validate_config(invalid_config)


# ✅ MOCKING & MOCK ASSERTIONS

def test_migrate_calls_client_create_source():
    """When migrate is called, it calls client.create_source exactly once."""
    # Setup: Create mock client
    client = _make_client()
    entry = _entry()

    # Execute: Call the function with mock
    # (In real test, would call the migration function)
    client.create_source(entry["source"])

    # Assert: Verify mock was called
    client.create_source.assert_called_once()


def test_migrate_calls_client_with_correct_arguments():
    """When migrate is called, it passes the correct data to client methods."""
    # Setup
    client = _make_client()
    entry = _entry(source_system="hubspot")

    # Execute
    client.create_source(entry["source"])

    # Assert: Verify called with specific arguments
    expected_call = entry["source"]
    client.create_source.assert_called_once_with(expected_call)


def test_dry_run_does_not_call_create():
    """When apply=False, create methods are not called."""
    # Setup
    client = _make_client()
    entry = _entry()

    # Execute: Simulate dry run (no actual creation)
    # ... (in real code, would call migrate(apply=False))

    # Assert: Verify methods were not called
    client.create_source.assert_not_called()
    client.create_destination.assert_not_called()


# ✅ USING MONKEYPATCH FOR ENVIRONMENT VARIABLES

def test_load_config_interpolates_env_vars(monkeypatch):
    """When config contains ${ENV_VAR}, it's replaced with environment value."""
    # Setup: Set environment variable and create config
    monkeypatch.setenv("AIRBYTE_URL", "https://airbyte.example.com")
    config_path = "/tmp/config.yaml"
    # (In real test, would create actual file with ${AIRBYTE_URL} reference)

    # Execute & Assert: (simplified for example)
    # result = load_config(config_path)
    # assert result["url"] == "https://airbyte.example.com"


def test_load_config_raises_on_missing_env_var(monkeypatch):
    """When config references missing env var, EnvironmentError is raised."""
    # Setup: Ensure variable is not set
    monkeypatch.delenv("MISSING_VAR", raising=False)

    # Execute & Assert: (simplified for example)
    # with pytest.raises(EnvironmentError, match="MISSING_VAR"):
    #     load_config(config_with_missing_var)


# ✅ GROUPING RELATED TESTS WITH COMMENTS

# --- load_config tests ---

def test_load_config_parses_yaml():
    """Verify YAML is parsed correctly."""
    pass


def test_load_config_handles_empty_file():
    """Verify empty YAML is handled gracefully."""
    pass


# --- validate_config tests ---

def test_validate_config_passes_valid():
    """Verify valid config passes validation."""
    pass


def test_validate_config_fails_invalid():
    """Verify invalid config raises error."""
    pass
