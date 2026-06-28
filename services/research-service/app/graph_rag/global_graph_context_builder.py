"""
Global Graph Context Builder.
"""

from app.graph_rag.global_graph_retriever import (
    retrieve_global_graph_context
)


def build_global_graph_context():

    graph_documents = (
        retrieve_global_graph_context()
    )

    return {

        "graph_documents":
        graph_documents
    }