"""
Pytest Fixtures & Configuration
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.config import TestingConfig
from backend.db.session import init_db, db_session as _db_session
from backend.models.base import Base
import backend.models  # noqa: F401


@pytest.fixture(scope="function")
def app():
    """Create and configure a new Flask app instance with in-memory SQLite for each test."""
    app = create_app(TestingConfig)

    with app.app_context():
        init_db(TestingConfig.SQLALCHEMY_DATABASE_URI, create_tables=True)
        yield app
        _db_session.rollback()
        _db_session.remove()
        from backend.db.session import engine
        Base.metadata.drop_all(bind=engine)


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
