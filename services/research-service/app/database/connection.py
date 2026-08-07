"""
Database connection.

Creates the SQLAlchemy engine
and session factory.
"""

import logging
from urllib.parse import quote_plus

from app.database.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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