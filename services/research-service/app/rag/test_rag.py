"""
Test Traditional RAG.
"""

from app.rag.rag_pipeline import (
    ask_question
)


def main():

    company_name = "HDFC Bank"

    while True:

        question = input(
            "\nAsk a question (type exit to quit): "
        ).strip()

        if question.lower() == "exit":

            break

        result = ask_question(
            question=question,
            company_name=company_name
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

        for i, doc in enumerate(result["documents"], start=1):

            print(f"\nChunk {i}")
            print("-" * 80)

            # Show first 700 characters
            print(doc[:700])

        print()

        print("=" * 100)
        print("RETRIEVAL INFO")
        print("=" * 100)

        print(f"Pipeline       : {result['pipeline']}")
        print(f"Chunks         : {result['num_chunks']}")
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