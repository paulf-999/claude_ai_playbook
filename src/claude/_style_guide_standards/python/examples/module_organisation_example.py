#!/usr/bin/env python3
"""
Description: YAML config loader with ${ENV_VAR} interpolation for the Airbyte manager
Date created: 2026-06-26

Demonstrates module organisation:
- Module docstring with Description and Date created
- __author__ and __version__ metadata
- Public functions (no underscore prefix)
- Private functions (underscore prefix)
- Constants grouped with comments
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import re
from typing import Any

import yaml

logger = None  # Would be actual logger in real code

# Regular expression for ${ENV_VAR} references
_ENV_VAR_RE = re.compile(r'\$\{([^}]+)\}')

# Migration action states
CREATE = "CREATE"
UPDATE = "UPDATE"
DISABLE = "DISABLE"
NOOP = "NOOP"

# Valid table descriptor values
_VALID_TABLE_DESCRIPTORS = {"small_tables", "medium_tables", "large_tables"}

# Default configuration values
DEFAULT_TIMEOUT = 30
DEFAULT_BATCH_SIZE = 100


# ✅ PUBLIC FUNCTIONS (no underscore prefix)
# These are the module's API — users import and call these

def load_config(path: str) -> dict:
    """Load YAML config and interpolate ${ENV_VAR} references.

    This is the main API for users of this module.

    Args:
        path: Path to YAML config file

    Returns:
        Parsed config dictionary with environment variables interpolated
    """
    with open(path) as f:
        raw = yaml.safe_load(f)
    return _interpolate(raw)


def validate_config(config: dict) -> None:
    """Validate config structure and required fields.

    Raises ValueError if config is invalid.
    """
    if "connections" in config:
        for conn in config["connections"]:
            td = conn.get("table_descriptor")
            if td and td not in _VALID_TABLE_DESCRIPTORS:
                raise ValueError(
                    f"Invalid table_descriptor '{td}'. Must be one of: {sorted(_VALID_TABLE_DESCRIPTORS)}"
                )


def apply_connection_names(config: dict) -> dict:
    """Derive connection names from source system and table descriptor.

    This is a public helper for transforming config.
    """
    return _apply_connection_names(config)


# ✅ PRIVATE FUNCTIONS (underscore prefix)
# These are internal helpers — not part of the public API

def _interpolate(obj: Any) -> Any:
    """Internal helper — recursively interpolate ${ENV_VAR} in strings."""
    if isinstance(obj, str):
        return _ENV_VAR_RE.sub(_sub_env_var, obj)
    elif isinstance(obj, dict):
        return {k: _interpolate(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_interpolate(item) for item in obj]
    return obj


def _sub_env_var(match) -> str:
    """Internal helper — substitute a single ${VAR} reference."""
    var_name = match.group(1)
    value = os.environ.get(var_name)
    if value is None:
        raise OSError(
            f"Environment variable '{var_name}' is not set (referenced in YAML config)"
        )
    return value


def _apply_connection_names(config: dict) -> dict:
    """Internal helper — derive connection names from source and table descriptor."""
    for source_system, source_config in config.items():
        if "connections" not in source_config:
            continue

        for conn in source_config["connections"]:
            if "table_descriptor" in conn:
                td = conn["table_descriptor"]
                conn["name"] = _derive_connection_name(source_system, td)

    return config


def _derive_connection_name(source_system: str, table_descriptor: str) -> str:
    """Internal helper — derive connection name from source and descriptor."""
    return f"{source_system}_{table_descriptor}"
