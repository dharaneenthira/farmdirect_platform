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
from backend.db import session as db_session_module
from backend.models.base import Base
import backend.models  # noqa: F401


@pytest.fixture
def app():
    """Create and configure a new Flask app instance for each test."""
    app = create_app(TestingConfig)

    with app.app_context():
        db_session_module.init_db(TestingConfig.SQLALCHEMY_DATABASE_URI, create_tables=True)
        yield app
        db_session_module.db_session.rollback()
        db_session_module.db_session.remove()
        Base.metadata.drop_all(bind=db_session_module.engine)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
