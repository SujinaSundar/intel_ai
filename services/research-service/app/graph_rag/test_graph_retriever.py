"""
Test graph retrieval.
"""

from app.graph_rag.graph_retriever import (
    retrieve_graph_context
)


def main():

    context = retrieve_graph_context(
        "Infosys"
    )

    print()

    print(
        "Graph Context"
    )

    print(
        "-" * 50
    )

    for item in context:

        print(
            item
        )


if __name__ == "__main__":

    main()