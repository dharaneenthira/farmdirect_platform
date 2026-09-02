"""
SQLAlchemy Engine and Session Management Architecture
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from flask import current_app, has_app_context
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from backend.config import get_config


def get_db_url():
    """Retrieve database URL from active Flask app context or fallback config."""
    if has_app_context() and "SQLALCHEMY_DATABASE_URI" in current_app.config:
        return current_app.config["SQLALCHEMY_DATABASE_URI"]
    return get_config().SQLALCHEMY_DATABASE_URI


def create_db_engine(uri=None):
    """Factory helper to build SQLAlchemy engine based on target URI."""
    if uri is None:
        uri = get_db_url()

    engine_kwargs = {"pool_pre_ping": True}
    if not uri.startswith("sqlite"):
        engine_kwargs.update({"pool_size": 10, "max_overflow": 20})

    return create_engine(uri, **engine_kwargs)


# Module-level default engine
engine = create_db_engine()

# Thread-safe Scoped Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)


def get_db():
    """Dependency helper to retrieve database session"""
    session = db_session()
    try:
        yield session
    finally:
        session.close()


def check_db_connection() -> bool:
    """
    Safely verifies database connectivity using a lightweight test query.
    Returns True if connected, False otherwise.
    """
    try:
        current_engine = db_session.get_bind()
        with current_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def init_db(target_engine=None):
    """Initialize database tables from registered SQLAlchemy models"""
    from backend.models import Base

    if target_engine is None:
        target_engine = db_session.get_bind()
    Base.metadata.create_all(bind=target_engine)
