"""
Graph Context Builder.
"""

from app.graph_rag.graph_retriever import (
    retrieve_graph_context
)


def build_graph_context(
    company_name: str
):
    """
    Build graph context.
    """

    graph_documents = (
        retrieve_graph_context(
            company_name
        )
    )

    return {

        "graph_documents":
        graph_documents
    }