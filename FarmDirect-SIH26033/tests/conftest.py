"""
Pytest Fixtures & Configuration
"""
import pytest
import sys
import os

# Ensure backend package can be imported during test runs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a new Flask app instance for each test."""
    app = create_app(TestingConfig)
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
