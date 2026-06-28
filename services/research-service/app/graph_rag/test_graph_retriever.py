"""
Test Graph Retriever.
"""

from app.graph_rag.graph_retriever import (
    retrieve_graph_context
)


def main():

    entity_name = input(
        "Enter entity name: "
    )

    results = retrieve_graph_context(
        entity_name
    )

    print()

    print(
        "Graph Context"
    )

    print(
        "-" * 80
    )

    for row in results:

        print(
            row
        )


if __name__ == "__main__":

    main()