"""
Test Hybrid Context Builder.
"""

from app.context_builder.hybrid_context_builder import (
    build_hybrid_context
)


def main() -> None:
    """
    Test hybrid context builder.
    """

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

    documents = context["documents"]

    for index, document in enumerate(
        documents,
        start=1
    ):

        print()

        print(
            f"Chunk {index}"
        )

        print(
            "-" * 80
        )

        print(
            document[:500]
        )

    sentiment = context["sentiment"]

    if sentiment:

        print()

        print(
            "Sentiment"
        )

        print(
            "-" * 80
        )

        print(
            f"Label: "
            f"{sentiment.sentiment_label}"
        )

        print(
            f"Confidence Score: "
            f"{sentiment.confidence_score}"
        )

    else:

        print()

        print(
            "No sentiment found."
        )

    stock = context["stock"]

    if stock:

        print()

        print(
            "Stock"
        )

        print(
            "-" * 80
        )

        print(
            f"Trade Date: "
            f"{stock.trade_date}"
        )

        print(
            f"Open Price: "
            f"{stock.open_price}"
        )

        print(
            f"High Price: "
            f"{stock.high_price}"
        )

        print(
            f"Low Price: "
            f"{stock.low_price}"
        )

        print(
            f"Close Price: "
            f"{stock.close_price}"
        )

        print(
            f"Volume: "
            f"{stock.volume}"
        )

    else:

        print()

        print(
            "No stock data found."
        )


if __name__ == "__main__":

    main()