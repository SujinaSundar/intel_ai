"""
Test GraphRAG.
"""

from app.graph_rag.graph_rag_pipeline import (
    ask_graph_question
)


def main():

    company_name = input(
        "Enter company name: "
    )

    while True:

        question = input(
            "\nAsk a question (type exit to quit): "
        )

        if question.lower() == "exit":

            break

        answer = ask_graph_question(

            question=question,

            company_name=company_name
        )

        print()

        print(
            "Answer"
        )

        print(
            "-" * 80
        )

        print(
            answer
        )


if __name__ == "__main__":

    main()