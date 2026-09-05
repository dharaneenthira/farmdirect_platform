"""
SQLAlchemy Engine and Session Management Architecture
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool
from backend.config import get_config

config = get_config()


def create_db_engine(uri=None):
    """Factory helper to build SQLAlchemy engine based on connection URI"""
    if uri is None:
        uri = config.SQLALCHEMY_DATABASE_URI

    kwargs = {}
    if uri.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
        if ":memory:" in uri:
            kwargs["poolclass"] = StaticPool
    else:
        kwargs["pool_pre_ping"] = True
        kwargs["pool_size"] = 10
        kwargs["max_overflow"] = 20

    return create_engine(uri, echo=getattr(config, "DEBUG", False), **kwargs)


engine = create_db_engine()

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


def init_db(uri=None, create_tables=True):
    """Initialize database tables architecture"""
    from backend.models.base import Base
    import backend.models  # noqa: F401

    global engine
    if uri:
        engine = create_db_engine(uri)
        db_session.configure(bind=engine)

    if create_tables:
        Base.metadata.create_all(bind=engine)
