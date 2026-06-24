"""
Test graph context builder.
"""

from app.graph_rag.graph_context_builder import (
    build_graph_context
)


def main():

    context = build_graph_context(
        "Infosys"
    )

    print()

    print(
        "Graph Context"
    )

    print(
        "-" * 80
    )

    for document in context[
        "graph_documents"
    ]:

        print(
            document
        )

    print()

    print(
        "Sentiment"
    )

    print(
        context["sentiment"]
    )

    print()

    print(
        "Stock"
    )

    print(
        context["stock"]
    )


if __name__ == "__main__":

    main()