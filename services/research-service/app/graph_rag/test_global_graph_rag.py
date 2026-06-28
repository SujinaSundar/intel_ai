"""
Test Global GraphRAG.
"""

from app.graph_rag.global_graph_rag_pipeline import (
    ask_global_graph_question
)


def main():

    while True:

        question = input(
            "\nQuestion (exit to quit): "
        )

        if question.lower() == "exit":

            break

        answer = ask_global_graph_question(
            question
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