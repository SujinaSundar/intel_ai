"""
Global Graph Retriever.
"""

from app.graph_rag.neo4j_service import (
    get_driver
)


def retrieve_global_graph_context(
    limit: int = 50
) -> list[str]:

    query = """
    MATCH (source)-[r]->(target)

    RETURN
        source.name AS source,
        type(r) AS relationship,
        target.name AS target

    LIMIT $limit
    """

    documents = []

    driver = get_driver()

    with driver.session() as session:

        results = session.run(
            query,
            limit=limit
        )

        for row in results:

            documents.append(
                f"{row['source']} "
                f"{row['relationship']} "
                f"{row['target']}"
            )

    return documents