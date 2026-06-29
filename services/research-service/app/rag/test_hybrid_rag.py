"""
Test Hybrid RAG.
"""

from app.rag.hybrid_rag_pipeline import (
    ask_hybrid_question
)


def main():

    while True:

        question = input(
            "\nAsk a question (type exit to quit): "
        ).strip()

        if question.lower() == "exit":

            break

        result = ask_hybrid_question(
            question=question
        )

        print()

        print("=" * 100)
        print("ANSWER")
        print("=" * 100)

        print(result["answer"])

        print()

        print("=" * 100)
        print("RETRIEVED DOCUMENTS")
        print("=" * 100)

        documents = result["documents"]

        metadata = result.get("metadata") or []

        for i, doc in enumerate(
            documents,
            start=1
        ):

            print(f"\nChunk {i}")
            print("-" * 80)

            if i <= len(metadata):

                info = metadata[i - 1]

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

                print("-" * 80)

            print(doc[:700])

        print()

        print("=" * 100)
        print("RETRIEVAL INFO")
        print("=" * 100)

        print(
            f"Pipeline       : {result['pipeline']}"
        )

        print(
            f"Chunks         : {result['num_chunks']}"
        )

        print(
            f"Retrieval Time : "
            f"{result['retrieval_time']:.2f} sec"
        )

        if result["sentiment"]:

            print("\nSentiment")

            print(result["sentiment"])

        if result["stock"]:

            print("\nStock")

            print(result["stock"])


if __name__ == "__main__":

    main()