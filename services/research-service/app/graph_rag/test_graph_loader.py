"""
Test graph loader.
"""

from app.graph_rag.graph_loader import (
    load_chunks
)


def main():

    chunks = load_chunks()

    print()

    print(
        "Total chunks:"
    )

    print(
        len(chunks)
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