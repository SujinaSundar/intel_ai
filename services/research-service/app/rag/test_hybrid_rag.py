"""
Test Hybrid RAG.
"""

from app.rag.hybrid_rag_pipeline import (
    ask_hybrid_question
)


def main() -> None:
    """
    Interactive Hybrid RAG testing.
    """

    company_name = input(
        "Enter company name: "
    ).strip()

    while True:

        question = input(
            "\nAsk a question (type exit to quit): "
        ).strip()

        if question.lower() == "exit":

            break

        answer = ask_hybrid_question(

            question=question,

            company_name=company_name
        )

        print()

        print(
            "Answer:"
        )

        print()

        print(
            answer
        )


if __name__ == "__main__":

    main()