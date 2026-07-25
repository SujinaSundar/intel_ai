"""
Neo4j Connection Service.

Provides a singleton Neo4j driver
for the Research Service.
"""

import logging
from typing import Optional

from neo4j import Driver, GraphDatabase
from neo4j.exceptions import Neo4jError

from app.database.config import settings
from app.exceptions.custom_exceptions import (
    DatabaseException,
)

logger = logging.getLogger(__name__)

_driver: Optional[Driver] = None


def get_driver() -> Driver:
    """
    Return a singleton Neo4j driver.

    The driver is initialized only once and
    reused across the application lifetime.

    Returns
    -------
    Driver
        Neo4j driver instance.
    """

    global _driver

    if _driver is None:

        logger.info(
            "Initializing Neo4j driver."
        )

        try:

            _driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(
                    settings.NEO4J_USERNAME,
                    settings.NEO4J_PASSWORD,
                ),
            )

            # Verify connectivity once during startup
            _driver.verify_connectivity()

            logger.info(
                "Connected to Neo4j successfully."
            )

        except Neo4jError as error:

            logger.exception(
                "Failed to connect to Neo4j."
            )

            raise DatabaseException(
                f"Neo4j connection failed: {error}"
            ) from error

    return _driver


def close_driver() -> None:
    """
    Close the Neo4j driver.

    This should be called during
    application shutdown.
    """

    global _driver

    if _driver is not None:

        logger.info(
            "Closing Neo4j driver."
        )

        _driver.close()

        _driver = None