"""
Test Graph Context Builder.
"""

from app.graph_rag.graph_context_builder import (
    build_context
)


def main():

    company_name = input(
        "Enter company name: "
    )

    context = build_context(
        company_name
    )

    print()

    print(
        "Graph Context"
    )

    print(
        "-" * 80
    )

    print(
        context
    )


if __name__ == "__main__":

    main()