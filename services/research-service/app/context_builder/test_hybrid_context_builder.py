"""
Test Hybrid Context Builder.
"""

from app.context_builder.hybrid_context_builder import (
    build_hybrid_context
)


def main():

    context = build_hybrid_context(

        question=
        "What is Infosys AI strategy?",

        company_name=
        "Infosys"
    )

    print()

    print(
        "Retrieved Documents"
    )

    print(
        "-" * 80
    )

    for index, document in enumerate(
        context["documents"],
        start=1
    ):

        print()

        print(
            f"Chunk {index}"
        )

        print(
            document[:500]
        )

    print()

    print(
        "Sentiment"
    )

    print(
        context["sentiment"]
    )

    print()

    print(
        "Stock"
    )

    print(
        context["stock"]
    )


if __name__ == "__main__":

    main()