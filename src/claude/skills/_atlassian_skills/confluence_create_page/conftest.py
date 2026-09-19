"""Adds this skill directory to sys.path so testing/ can import confluence_create_page_handler.py.

Pytest inserts any directory containing a conftest.py into sys.path, which is
what lets testing/test_*.py use bare `from confluence_create_page_handler
import ...` despite living one level below the handler.
"""
