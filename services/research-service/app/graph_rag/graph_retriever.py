"""
Graph retrieval service.
"""

from app.graph_rag.neo4j_service import (
    get_driver
)


def retrieve_graph_context(
    company_name: str
) -> list[str]:
    """
    Retrieve graph information.

    Parameters
    ----------
    company_name : str

    Returns
    -------
    list[str]
    """

    driver = get_driver()

    with driver.session() as session:

        result = session.run(
            """
            MATCH (c:Company {name:$company_name})-[r]->(n)

            RETURN
                c.name AS company,
                type(r) AS relationship,
                n.name AS entity
            """,

            company_name=company_name
        )

        context = []

        for record in result:

            sentence = (
                f"{record['company']} "
                f"{record['relationship']} "
                f"{record['entity']}"
            )

            context.append(
                sentence
            )

    return context