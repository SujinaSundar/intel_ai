"""
Test retrieval layer.
"""

from app.retrieval.retrieval_service import (
    retrieve_documents
)


def main() -> None:
    """
    Test ChromaDB retrieval.
    """

    query = (
        "What are Infosys AI investments?"
    )

    documents = retrieve_documents(
        query=query,
        top_k=5
    )

    print()

    for index, document in enumerate(
        documents,
        start=1
    ):

        print(
            f"\nChunk {index}"
        )

        print(
            "-" * 80
        )

        print(
            document[:500]
        )


if __name__ == "__main__":

    main()