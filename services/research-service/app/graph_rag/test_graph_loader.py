"""
Test Graph Loader.
"""

from app.graph_rag.graph_loader import (
    load_company_chunks
)


def main():

    chunks = load_company_chunks(
        "TCS"
    )

    print()

    print(
        f"Total chunks: {len(chunks)}"
    )
    for i in range(5):
        print(f"Chunk {i+1}")
        print("-" * 80)

        print(
            chunks[i][:300]
        )
    print()

    print(
        "First chunk"
    )

    print(
        "-" * 80
    )

    print(
        chunks[0][:500]
    )


if __name__ == "__main__":

    main()