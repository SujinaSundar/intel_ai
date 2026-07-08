"""
Hybrid Graph Context Builder.

Combines Hybrid RAG retrieval
and GraphRAG retrieval.
"""

from app.context_builder.hybrid_context_builder import (
    build_hybrid_context
)

from app.graph_rag.graph_context_builder import (
    build_graph_context
)


def build_hybrid_graph_context(
    question: str,
    company_name: str
) -> dict:
    """
    Build Hybrid GraphRAG context.

    Parameters
    ----------
    question : str

    company_name : str

    Returns
    -------
    dict
    """

    # -----------------------------------
    # Hybrid RAG Context
    # -----------------------------------

    hybrid_context = (

        build_hybrid_context(

            question=question,

            company_name=company_name

        )

    )

    # -----------------------------------
    # Graph Context
    # -----------------------------------

    graph_context = (

    build_graph_context(

        question=question,

        company_name=company_name

    )

)
    # -----------------------------------
    # Combined Context
    # -----------------------------------

    return {

        "documents":

            hybrid_context["documents"],

        "metadata":

            hybrid_context["metadata"],

        "sentiment":

            hybrid_context["sentiment"],

        "stock":

            hybrid_context["stock"],

        "graph_documents":

            graph_context["graph_documents"]

    }