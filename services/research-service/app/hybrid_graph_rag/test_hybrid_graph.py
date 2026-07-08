"""
Test Hybrid GraphRAG.
"""

from app.hybrid_graph_rag.hybrid_graph_pipeline import (
    ask_hybrid_graph_question
)


def main():
    """
    Interactive Hybrid GraphRAG testing.
    """

    while True:

        question = input(
            "\nAsk a question (type exit to quit): "
        ).strip()

        if question.lower() == "exit":

            break

        result = ask_hybrid_graph_question(
            question
        )

        print()

        print("=" * 100)
        print("ANSWER")
        print("=" * 100)

        print(
            result["answer"]
        )

        print()

        print("=" * 100)
        print("DOCUMENT CONTEXT")
        print("=" * 100)

        documents = result[
            "documents"
        ]

        if not documents:

            print(
                "No document context found."
            )

        else:

            for index, document in enumerate(

                documents,

                start=1

            ):

                print()

                print(
                    f"Document {index}"
                )

                print(
                    "-" * 80
                )

                print(
                    document
                )

        print()

        print("=" * 100)
        print("GRAPH CONTEXT")
        print("=" * 100)

        graph_context = result[
            "graph_context"
        ]

        if not graph_context:

            print(
                "No graph context found."
            )

        else:

            for index, triple in enumerate(

                graph_context,

                start=1

            ):

                print()

                print(
                    f"Triple {index}"
                )

                print(
                    "-" * 80
                )

                print(
                    triple
                )

        print()

        print("=" * 100)
        print("RETRIEVAL INFO")
        print("=" * 100)

        print(
            f"Pipeline       : {result['pipeline']}"
        )

        print(
            f"Company        : {result['company_name']}"
        )

        print(
            f"Documents      : {result['num_chunks']}"
        )

        print(
            f"Graph Triples  : {result['num_triples']}"
        )

        print(
            f"Retrieval Time : "
            f"{result['retrieval_time']:.2f} sec"
        )


if __name__ == "__main__":

    main()