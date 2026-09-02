"""
SQLAlchemy Engine and Session Management Architecture
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from backend.config import get_config

config = get_config()

# SQLAlchemy Engine Initialization (Lazy/Config-driven)
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=config.DEBUG,
)

# Thread-safe Scoped Session Factory
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_db():
    """Dependency helper to retrieve database session"""
    session = db_session()
    try:
        yield session
    finally:
        session.close()


def init_db():
    """Initialize database tables architecture placeholder"""
    from backend.models.base import Base

    Base.metadata.create_all(bind=engine)
