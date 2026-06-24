"""
RAG pipeline.
"""

from app.context_builder.context_builder import (
    build_context
)

from app.prompts.prompt_template import (
    build_prompt
)

from app.llm.llm_service import (
    generate_answer
)


def ask_question(
    question: str,
    company_name: str
) -> str:
    """
    Execute RAG pipeline.

    Parameters
    ----------
    question : str

    company_name : str

    Returns
    -------
    str
    """

    context = build_context(
        question=question,
        company_name=company_name
    )

    documents = context["documents"]

    sentiment = context["sentiment"]

    stock = context["stock"]

    sentiment_text = "No sentiment found"

    if sentiment:

        sentiment_text = (
            f"{sentiment.sentiment_label} "
            f"({sentiment.confidence_score:.2f})"
        )

    stock_text = "No stock data found"

    if stock:

        stock_text = (
            f"Close Price: {stock.close_price}\n"
            f"Volume: {stock.volume}"
        )

    prompt = build_prompt(
        question=question,
        documents=documents,
        sentiment=sentiment_text,
        stock_data=stock_text
    )

    answer = generate_answer(
        prompt
    )

    return answer