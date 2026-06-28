"""
Test Global Graph Retriever.
"""

from app.graph_rag.global_graph_retriever import (
    retrieve_global_graph_context
)


def main():

    docs = retrieve_global_graph_context()

    print()

    print(
        f"Relationships: {len(docs)}"
    )

    print()

    for doc in docs[:20]:

        print(doc)


if __name__ == "__main__":

    main()