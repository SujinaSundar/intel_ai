"""
Test Neo4j connection.
"""

from app.graph_rag.neo4j_service import (
    get_driver
)


def main():

    driver = get_driver()

    with driver.session() as session:

        result = session.run(

            "RETURN 'Connected to Neo4j' AS message"
        )

        for record in result:

            print(

                record["message"]
            )


if __name__ == "__main__":

    main()