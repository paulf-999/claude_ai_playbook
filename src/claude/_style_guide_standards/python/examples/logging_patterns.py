#!/usr/bin/env python3
"""
Example: Logging patterns from logging/*.md

Demonstrates:
- Logger setup at module level
- Log levels: DEBUG, INFO, WARNING, ERROR
- What to log: entry/exit, state changes, counts
- What NOT to log: secrets, PII, full tracebacks
- Logging in error handling
"""

import logging
import os

logger = logging.getLogger(__name__)


# ✅ GOOD: Logger setup at module level (never in functions)
# This is the correct pattern — allows granular control per module


# ✅ GOOD: DEBUG — development details

def process_migration(plan_path: str, apply: bool):
    """Process migration with appropriate logging at each level."""
    logger.debug(f"Loading plan from: {plan_path}")
    logger.debug(f"Apply mode: {apply}")

    try:
        plan = load_plan(plan_path)
        logger.debug(f"Plan loaded with {len(plan)} connections")
    except Exception as e:
        logger.error(f"Failed to load plan: {e}")
        raise


# ✅ GOOD: INFO — progress and results

def migrate_connections(client, connections: list) -> int:
    """Migrate connections with INFO-level progress logging."""
    logger.info(f"Starting migration of {len(connections)} connections")

    created = 0
    for conn in connections:
        try:
            client.create_connection(conn)
            created += 1
        except Exception as e:
            logger.error(f"Failed to create connection '{conn.get('name')}': {e}")
            continue

    logger.info(f"Migration complete: {created} connections created")
    return created


# ✅ GOOD: WARNING — unexpected but recoverable

def get_connection_by_name(client, name: str):
    """Get connection with fallback; log warning if fallback used."""
    try:
        return client.get_connection(name)
    except ConnectionNotFoundError:
        logger.warning(
            f"Connection '{name}' not found on target server, using fallback 'default'"
        )
        return client.get_connection("default")


# ✅ GOOD: ERROR — log before raising exception

def load_required_var(var_name: str) -> str:
    """Load required env var; log error before raising."""
    value = os.environ.get(var_name)
    if value is None:
        logger.error(f"Required environment variable '{var_name}' is not set")
        raise OSError(f"{var_name} is not set")
    return value


# ✅ GOOD: What to log — entry/exit for important functions

def reconcile_config(desired: dict, actual: dict) -> dict:
    """Reconcile config with logging at entry and exit."""
    logger.info(f"Reconciling config: {len(desired)} desired vs {len(actual)} actual")

    changes = {}
    for key, value in desired.items():
        if key not in actual:
            changes[key] = "CREATE"
            logger.debug(f"Will create: {key}")
        elif actual[key] != value:
            changes[key] = "UPDATE"
            logger.debug(f"Will update: {key}")

    logger.info(f"Reconciliation complete: {len(changes)} changes needed")
    return changes


# ✅ GOOD: Log amounts/counts

def process_batch(items: list, batch_size: int = 100):
    """Process items in batches with progress logging."""
    logger.info(f"Processing {len(items)} items in batches of {batch_size}")

    for i, item in enumerate(items, 1):
        if i % batch_size == 0:
            logger.info(f"Processed {i}/{len(items)} items")
        # Process item


# ❌ BAD: What NOT to log — secrets and credentials

def bad_logging_example():
    """DO NOT do this — logs secrets/PII."""
    # ❌ WRONG — exposes credentials
    api_key = "sk-abc123xyz"
    logger.debug(f"Using API key: {api_key}")

    # ❌ WRONG — exposes connection string
    db_connection = "postgres://user:password@host:5432/db"
    logger.debug(f"Connecting to: {db_connection}")

    # ❌ WRONG — exposes customer data
    customer_email = "customer@example.com"
    logger.info(f"Processing customer: {customer_email}")


# ✅ GOOD: What TO log instead of secrets

def good_logging_example():
    """Correct logging without secrets/PII."""
    # ✅ GOOD — no credentials
    logger.debug(f"Using configured API credentials")

    # ✅ GOOD — no connection string
    logger.debug(f"Connecting to database at postgres-01.prod")

    # ✅ GOOD — customer identified by ID only
    customer_id = "cust-12345"
    logger.info(f"Processing customer ID: {customer_id}")


# ❌ BAD: Excessive DEBUG logs (creates noise)

def bad_debug_logging():
    """DO NOT log every iteration in loops."""
    items = list(range(100000))

    # ❌ WRONG — 100K log lines!
    for item in items:
        logger.debug(f"Processing item: {item}")


# ✅ GOOD: Log periodically or at summary

def good_debug_logging():
    """Log periodically for long operations."""
    items = list(range(100000))

    for i, item in enumerate(items, 1):
        if i % 1000 == 0:
            logger.debug(f"Processed {i}/{len(items)} items...")
        # Process item

    logger.debug(f"Completed processing all {len(items)} items")


# ✅ GOOD: Logging in error handling — always log before re-raising

def load_config_with_logging(config_path: str) -> dict:
    """Load config with proper error logging."""
    try:
        with open(config_path) as f:
            import yaml
            config = yaml.safe_load(f)
        logger.debug(f"Successfully loaded config from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {config_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading config from {config_path}: {e}")
        raise
