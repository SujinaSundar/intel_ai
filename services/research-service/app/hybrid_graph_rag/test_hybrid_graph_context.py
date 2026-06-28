"""
Test Hybrid Graph Context.
"""

from app.hybrid_graph_rag.hybrid_graph_context_builder import (
    build_hybrid_graph_context
)


def main():

    context = build_hybrid_graph_context(

        question=
        "What does HDFC Bank focus on?",

        company_name=
        "HDFC Bank"
    )

    print()

    print(
        "Documents:",
        len(
            context["documents"]
        )
    )

    print()

    print(
        "Graph Relationships:",
        len(
            context[
                "graph_documents"
            ]
        )
    )

    print()

    print(
        context[
            "graph_documents"
        ][:5]
    )


if __name__ == "__main__":

    main()