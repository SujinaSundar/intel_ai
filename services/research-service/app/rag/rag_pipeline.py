"""
RAG pipeline.
"""

import time

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
) -> dict:
    """
    Execute RAG pipeline.

    Parameters
    ----------
    question : str

    company_name : str

    Returns
    -------
    dict
    """

    # -----------------------------
    # Retrieval
    # -----------------------------

    start_time = time.perf_counter()

    context = build_context(
        question=question,
        company_name=company_name
    )

    retrieval_time = (
        time.perf_counter() - start_time
    )

    documents = context["documents"]

    sentiment = context["sentiment"]

    stock = context["stock"]

    # -----------------------------
    # Sentiment
    # -----------------------------

    sentiment_text = "No sentiment found"

    sentiment_data = None

    if sentiment:

        sentiment_text = (
            f"{sentiment.sentiment_label} "
            f"({sentiment.confidence_score:.2f})"
        )

        sentiment_data = {

            "label": sentiment.sentiment_label,

            "confidence": sentiment.confidence_score

        }

    # -----------------------------
    # Stock
    # -----------------------------

    stock_text = "No stock data found"

    stock_data = None

    if stock:

        stock_text = (
            f"Close Price: {stock.close_price}\n"
            f"Volume: {stock.volume}"
        )

        stock_data = {

            "trade_date": str(
                stock.trade_date
            ),

            "close_price": stock.close_price,

            "volume": stock.volume

        }

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = build_prompt(
        question=question,
        documents=documents,
        sentiment=sentiment_text,
        stock_data=stock_text
    )

    # -----------------------------
    # LLM
    # -----------------------------

    answer = generate_answer(
        prompt
    )

    # -----------------------------
    # Return
    # -----------------------------

    return {

        "pipeline": "Traditional RAG",

        "question": question,

        "answer": answer,

        "documents": documents,

        "graph_context": [],

        "sentiment": sentiment_data,

        "stock": stock_data,

        "retrieval_time": retrieval_time,

        "num_chunks": len(documents)

    }