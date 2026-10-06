#!/usr/bin/env python3
"""
Example: Error handling patterns from logging/_error_handling.md

Demonstrates:
- Logging before re-raising exceptions
- Specific exception types
- Logging at appropriate levels
- Using finally for cleanup
"""

import os
import yaml
import logging

logger = logging.getLogger(__name__)


# ✅ GOOD: Always log before re-raising — provides debugging context
def load_config(config_path: str) -> dict:
    """Load YAML config file with error context."""
    try:
        with open(config_path) as f:
            raw = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {config_path}: {e}")
        raise
    return raw


# ✅ GOOD: Specific exception types — not generic Exception
def load_required_var(var_name: str) -> str:
    """Load required environment variable with specific error type."""
    value = os.environ.get(var_name)
    if value is None:
        logger.error(f"Required environment variable '{var_name}' is not set")
        raise OSError(f"{var_name} is not set")
    return value


# ✅ GOOD: Use appropriate log level for error context
def validate_config(config: dict) -> None:
    """Validate config; expected errors use WARNING, unexpected use ERROR."""
    # Expected validation error — WARNING level
    if "connections" not in config:
        logger.warning("Config missing 'connections' section, using empty list")
        return

    # Unexpected system error — ERROR level
    try:
        for conn in config["connections"]:
            if "name" not in conn:
                logger.error("Connection missing required field 'name'")
                raise ValueError("Connection missing required field 'name'")
    except (KeyError, TypeError) as e:
        logger.error(f"Invalid config structure: {e}")
        raise


# ✅ GOOD: Use finally for guaranteed cleanup with logging
class Client:
    """Example client with cleanup."""

    def __init__(self):
        self.connected = True

    def migrate(self, data):
        """Migrate data with guaranteed cleanup."""
        try:
            logger.info("Starting migration")
            # Simulate work
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise
        finally:
            try:
                self.close()
                logger.debug("Client closed successfully")
            except Exception as e:
                logger.warning(f"Error closing client: {e}")

    def close(self):
        """Close the client."""
        self.connected = False
