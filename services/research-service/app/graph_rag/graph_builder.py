"""
Graph builder.

Creates nodes and relationships in Neo4j.
"""

import re

from app.graph_rag.neo4j_service import (
    get_driver
)


def normalize_label(label: str) -> str:
    """
    Normalize Neo4j labels.

    Neo4j labels cannot contain spaces
    or special characters.
    """

    label = label.strip()

    label = label.replace(" ", "_")

    label = label.replace("-", "_")

    label = re.sub(
        r"[^A-Za-z0-9_]",
        "",
        label
    )

    if not label:

        label = "Entity"

    return label


def create_node(
    label: str,
    name: str
):
    """
    Create graph node.
    """

    if not name:

        return

    label = normalize_label(label)

    driver = get_driver()

    with driver.session() as session:

        session.run(

            f"""
            MERGE (n:{label} {{
                name:$name
            }})

            ON CREATE SET

                n.created_at=datetime(),

                n.label=$label
            """,

            name=name,

            label=label
        )


def create_relationship(
    source: str,
    relationship: str,
    target: str
):
    """
    Create relationship.
    """

    if not source or not target:

        return

    relationship = normalize_label(
        relationship
    ).upper()

    driver = get_driver()

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

            target=target
        )


def clear_graph():
    """
    Delete graph.
    """

    driver = get_driver()

    with driver.session() as session:

        session.run(

            """
            MATCH (n)

            DETACH DELETE n
            """
        )


def get_node_count():

    driver = get_driver()

    with driver.session() as session:

        result = session.run(

            """
            MATCH (n)

            RETURN count(n) AS count
            """
        )

        return result.single()["count"]


def get_relationship_count():

    driver = get_driver()

    with driver.session() as session:

        result = session.run(

            """
            MATCH ()-[r]->()

            RETURN count(r) AS count
            """
        )

        return result.single()["count"]