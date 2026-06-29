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

    result = retrieve_documents(

        query=query,

        top_k=5

    )

    documents = result["documents"]

    metadata = result["metadata"]

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

        if index <= len(metadata):

            info = metadata[index - 1]

            print(
                f"Company     : {info.get('company_name', 'N/A')}"
            )

            print(
                f"Report Type : {info.get('report_type', 'N/A')}"
            )

            print(
                f"Year        : {info.get('year', 'N/A')}"
            )

            print(
                f"Chunk No.   : {info.get('chunk_number', 'N/A')}"
            )

            print(
                "-" * 80
            )

        print(
            document[:500]
        )


if __name__ == "__main__":

    main()