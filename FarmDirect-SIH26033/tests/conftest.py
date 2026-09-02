"""
Pytest Fixtures & Configuration
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.config import TestingConfig
from backend.db.session import db_session as _db_session
from backend.models import Base


@pytest.fixture(scope="function")
def app():
    """Create and configure a new Flask app instance with in-memory SQLite for each test."""
    app = create_app(TestingConfig)

    # Use single-connection StaticPool for in-memory SQLite during unit tests
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    _db_session.configure(bind=test_engine)

    with app.app_context():
        Base.metadata.create_all(bind=test_engine)
        yield app
        Base.metadata.drop_all(bind=test_engine)
        _db_session.remove()


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Provides a clean database session fixture for testing."""
    session = _db_session()
    yield session
    session.rollback()
    session.close()
