"""
Test Hybrid GraphRAG.
"""

from app.hybrid_graph_rag.hybrid_graph_pipeline import (
    ask_hybrid_graph_question
)


def main():

    answer = ask_hybrid_graph_question(

        question=
        "What policies are associated with HDFC Bank?",

        company_name=
        "HDFC Bank"
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