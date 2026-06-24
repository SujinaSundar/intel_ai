"""
Test BM25 retrieval.
"""

from app.hybrid_retrieval.bm25_service import (
    bm25_retrieve
)


def main():

    documents = bm25_retrieve(

        query=
        "What is Infosys AI strategy?",

        top_k=5
    )

    for index, document in enumerate(
        documents,
        start=1
    ):

        print()

        print(
            f"Chunk {index}"
        )

        print(
            "-" * 80
        )

        print(
            document
        )


if __name__ == "__main__":

    main()