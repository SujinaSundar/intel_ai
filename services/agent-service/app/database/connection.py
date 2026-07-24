"""
Database configuration.

Creates the SQLAlchemy
engine and provides
database sessions for
the application.
"""

import logging
from collections.abc import Generator
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.config import settings

logger = logging.getLogger(__name__)

# -----------------------------------------------------
# Database URL
# -----------------------------------------------------

password = quote_plus(
    settings.POSTGRES_PASSWORD
)

DATABASE_URL = (
    f"postgresql://"
    f"{settings.POSTGRES_USER}:"
    f"{password}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

# -----------------------------------------------------
# SQLAlchemy Engine
# -----------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
)

logger.info(
    "Database engine initialized."
)

# -----------------------------------------------------
# Session Factory
# -----------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# -----------------------------------------------------
# Database Dependency
# -----------------------------------------------------


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session.

    Yields
    ------
    Session
        SQLAlchemy database session.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()