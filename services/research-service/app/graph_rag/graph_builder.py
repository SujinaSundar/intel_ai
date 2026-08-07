"""
Graph Builder.

Creates and manages nodes and
relationships in Neo4j.
"""

import logging
import re

from app.exceptions.custom_exceptions import (
    DatabaseException,
    InvalidRequestException,
)
from app.graph_rag.neo4j_service import (
    get_driver,
)
from neo4j.exceptions import Neo4jError

logger = logging.getLogger(__name__)


def normalize_label(label: str) -> str:
    """
    Normalize Neo4j labels.

    Neo4j labels cannot contain spaces
    or special characters.
    """

    if not label.strip():
        return "Entity"

    label = label.strip()

    label = label.replace(" ", "_")
    label = label.replace("-", "_")

    label = re.sub(
        r"[^A-Za-z0-9_]",
        "",
        label,
    )

    return label or "Entity"


def create_node(
    label: str,
    name: str,
) -> None:
    """
    Create a graph node.
    """

    if not name.strip():
        raise InvalidRequestException(
            "Node name cannot be empty."
        )

    label = normalize_label(label)

    logger.info(
        "Creating node '%s' with label '%s'.",
        name,
        label,
    )

    driver = get_driver()

    try:

        with driver.session() as session:

            session.run(
                f"""
                MERGE (n:{label} {{
                    name:$name
                }}

                )

                ON CREATE SET
                    n.created_at=datetime(),
                    n.label=$label
                """,
                name=name,
                label=label,
            )

    except Neo4jError as error:

        logger.exception(
            "Failed to create node."
        )

        raise DatabaseException(
            f"Neo4j node creation failed: {error}"
        ) from error


def create_relationship(
    source: str,
    relationship: str,
    target: str,
) -> None:
    """
    Create a relationship between
    two existing nodes.
    """

    if not source.strip():
        raise InvalidRequestException(
            "Source node cannot be empty."
        )

    if not target.strip():
        raise InvalidRequestException(
            "Target node cannot be empty."
        )

    relationship = normalize_label(
        relationship
    ).upper()

    logger.info(
        "Creating relationship %s -> %s (%s).",
        source,
        target,
        relationship,
    )

    driver = get_driver()

    try:

        with driver.session() as session:

            session.run(
                f"""
                MATCH (a {{name:$source}})
                MATCH (b {{name:$target}})

                MERGE (a)-[r:{relationship}]->(b)

                ON CREATE SET
                    r.created_at=datetime()
                """,
                source=source,
                target=target,
            )

    except Neo4jError as error:

        logger.exception(
            "Failed to create relationship."
        )

        raise DatabaseException(
            f"Neo4j relationship creation failed: {error}"
        ) from error


def clear_graph() -> None:
    """
    Delete all nodes and relationships.
    """

    logger.warning(
        "Clearing Neo4j graph."
    )

    driver = get_driver()

    try:

        with driver.session() as session:

            session.run(
                """
                MATCH (n)
                DETACH DELETE n
                """
            )

    except Neo4jError as error:

        logger.exception(
            "Failed to clear graph."
        )

        raise DatabaseException(
            f"Failed to clear graph: {error}"
        ) from error


def get_node_count() -> int:
    """
    Return the number of nodes.
    """

    driver = get_driver()

    try:

        with driver.session() as session:

            result = session.run(
                """
                MATCH (n)
                RETURN count(n) AS count
                """
            )

            count = result.single()["count"]

            logger.info(
                "Node count: %d",
                count,
            )

            return count

    except Neo4jError as error:

        logger.exception(
            "Failed to retrieve node count."
        )

        raise DatabaseException(
            f"Failed to retrieve node count: {error}"
        ) from error


def get_relationship_count() -> int:
    """
    Return the number of relationships.
    """

    driver = get_driver()

    try:

        with driver.session() as session:

            result = session.run(
                """
                MATCH ()-[r]->()
                RETURN count(r) AS count
                """
            )

            count = result.single()["count"]

            logger.info(
                "Relationship count: %d",
                count,
            )

            return count

    except Neo4jError as error:

        logger.exception(
            "Failed to retrieve relationship count."
        )

        raise DatabaseException(
            f"Failed to retrieve relationship count: {error}"
        ) from error