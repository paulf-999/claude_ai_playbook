# 🔧 Pytest Fixtures & Mocking

**Purpose:** Establish fixtures and mocking conventions for isolating code under test and reducing duplication.

---

## 🔧 Pytest fixtures

**Common fixtures from pytest:**

### `monkeypatch` — Mock environment variables and module attributes

```python
def test_parse_args_defaults(monkeypatch):
    # Override sys.argv for this test
    monkeypatch.setattr("sys.argv", ["airbyte_connection_creator.py"])
    args = parse_args()
    assert args.config is None
```

### `tmp_path` — Create temporary directory for test files

```python
def test_run_dry_run_plans_but_does_not_create(tmp_path):
    # Create temp files for test
    inventory_path = tmp_path / "connection_inventory.yaml"
    log_path = tmp_path / "connection_migration_log.yaml"
    inventory_path.write_text("...")

    # Run the function
    ConnectionMigrator(client).run(
        apply=False,
        inventory_path=str(inventory_path),
        log_path=str(log_path),
    )

    # Assert log file was not created
    assert not log_path.exists()
```

### Custom fixtures — Helper functions for test setup

Create underscore-prefixed helper functions to set up test data:

```python
def _make_client():
    """Create mock Airbyte client with default return values."""
    client = MagicMock()
    client.base_url = "https://test-server.prod.payroc.com:8006"
    client.list_sources.return_value = []
    client.list_destinations.return_value = []
    return client


def _entry(source_system="salesforce_prod", source_server="dc1_source_1"):
    """Create a sample connection entry for testing."""
    return {
        "source_server": source_server,
        "source_system": source_system,
        "source": {"name": "Salesforce Prod", "connector_type": "source-salesforce"},
        "destination": {"name": "Snowflake Raw", "connector_type": "destination-snowflake"},
    }


def test_migrate_creates_source(tmp_path):
    # Setup: use helper to create consistent test data
    client = _make_client()
    entry = _entry(source_system="salesforce_prod")

    # Execute and assert
    ConnectionMigrator(client).process(entry)
    client.create_source.assert_called_once()
```

**Why:** Underscore-prefixed helpers reduce duplication and make tests more readable.

---

## 🎭 Mocking

**Use `MagicMock` for external dependencies:**

```python
from unittest.mock import MagicMock

def test_migrate_calls_client_create_source(tmp_path):
    client = MagicMock()
    client.create_source.return_value = {"sourceId": "s1"}

    # When we call migrate, it should call client.create_source
    ConnectionMigrator(client).migrate(entry)

    # Assert the mock was called
    client.create_source.assert_called_once()
```

### Mock assertions — verify interactions

```python
# Assert called exactly once
client.create_source.assert_called_once()

# Assert called with specific arguments
client.create_source.assert_called_once_with({"name": "Salesforce"})

# Assert not called
client.create_source.assert_not_called()

# Assert called N times
assert client.create_source.call_count == 3
```

**Why:** Mocking isolates the code being tested from its dependencies. Mock assertions verify the code interacts with dependencies correctly.

---

## 🔗 Related

- Parent: `testing.md` — Testing conventions overview
- Sibling: `testing/_naming_structure.md` — Test naming and structure
- Sibling: `testing/_assertions.md` — Assertions and exception testing
