"""
ChromaDB Client.

Initializes the ChromaDB client and
provides access to the financial reports collection.
"""

import logging

import chromadb

from app.database.config import settings
from app.exceptions.custom_exceptions import (
    DatabaseException,
)

logger = logging.getLogger(__name__)

logger.info("Initializing ChromaDB client.")

try:

    client = chromadb.PersistentClient(
        path=settings.CHROMA_DB_PATH,
    )

    collection = client.get_or_create_collection(
        name=settings.CHROMA_COLLECTION_NAME,
    )

    logger.info(
        "Connected to ChromaDB collection: %s",
        settings.CHROMA_COLLECTION_NAME,
    )

except Exception as error:

    logger.exception(
        "Failed to initialize ChromaDB."
    )

    raise DatabaseException(
        f"Failed to initialize ChromaDB: {error}"
    ) from error