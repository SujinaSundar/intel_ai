"""
Graph builder.

Creates nodes and relationships in Neo4j.
"""

from app.graph_rag.neo4j_service import (
    get_driver
)


def create_node(
    label: str,
    name: str
):
    """
    Create graph node.

    Parameters
    ----------
    label : str

    name : str
    """

    driver = get_driver()

    with driver.session() as session:

        session.run(

            f"""
            MERGE (n:{label}
            {{
                name:$name
            }})
            """,

            name=name
        )


def create_relationship(
    source: str,
    relationship: str,
    target: str
):
    """
    Create relationship.

    Parameters
    ----------
    source : str

    relationship : str

    target : str
    """

    driver = get_driver()

    with driver.session() as session:

        session.run(

            f"""
            MATCH (a {{name:$source}})
            MATCH (b {{name:$target}})

            MERGE (a)-[:{relationship}]->(b)
            """,

            source=source,

            target=target
        )


def clear_graph():
    """
    Delete all nodes and relationships.
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
    """
    Get total node count.
    """

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
    """
    Get total relationship count.
    """

    driver = get_driver()

    with driver.session() as session:

        result = session.run(

            """
            MATCH ()-[r]->()

            RETURN count(r) AS count
            """
        )

        return result.single()["count"]