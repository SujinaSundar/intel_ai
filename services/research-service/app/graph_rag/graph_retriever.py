"""
Graph retriever.
"""

from app.graph_rag.neo4j_service import (
    get_driver
)


def retrieve_graph_context(
    entity_name: str
) -> list[str]:
    """
    Retrieve graph context.
    """

    driver = get_driver()

    with driver.session() as session:

        result = session.run(

            """
            MATCH (a)-[r]->(b)

            WHERE a.name = $name

            RETURN
                a.name,
                type(r),
                b.name
            """,

            name=entity_name
        )

        context = set()

        for row in result:

            context.add(

                f"{row[0]} "
                f"{row[1]} "
                f"{row[2]}"
            )

        return list(context)