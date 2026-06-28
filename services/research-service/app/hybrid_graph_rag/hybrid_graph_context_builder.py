"""
Hybrid Graph Context Builder.
"""

from app.context_builder.hybrid_context_builder import (
    build_hybrid_context
)

from app.graph_rag.graph_context_builder import (
    retrieve_graph_context
)


def build_hybrid_graph_context(
    question: str,
    company_name: str
) -> dict:
    """
    Combine Hybrid RAG context
    and GraphRAG context.
    """

    hybrid_context = (
        build_hybrid_context(
            question=question,
            company_name=company_name
        )
    )

    graph_documents = (
        retrieve_graph_context(
            company_name
        )
    )

    return {

        "documents":
        hybrid_context["documents"],

        "sentiment":
        hybrid_context["sentiment"],

        "stock":
        hybrid_context["stock"],

        "graph_documents":
        graph_documents
    }