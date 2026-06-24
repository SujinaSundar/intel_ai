"""
Manual retrieval evaluation.
"""

from app.evaluation.questions import (
    questions
)

from app.retrieval.retrieval_service import (
    retrieve_documents
)


def evaluate() -> None:

    for index, question in enumerate(
        questions,
        start=1
    ):

        print(
            "\n" + "=" * 100
        )

        print(
            f"Question {index}"
        )

        print(
            question
        )

        print(
            "=" * 100
        )

        documents = retrieve_documents(
            query=question,
            top_k=5
        )

        for i, document in enumerate(
            documents,
            start=1
        ):

            print(
                f"\nChunk {i}"
            )

            print(
                "-" * 80
            )

            print(
                document[:500]
            )


if __name__ == "__main__":

    evaluate()