"""
Hybrid RAG pipeline.
"""

import time

from app.context_builder.hybrid_context_builder import (
    build_hybrid_context
)

from app.prompts.hybrid_prompt_template import (
    build_hybrid_prompt
)

from app.llm.llm_service import (
    generate_answer
)


def ask_hybrid_question(
    question: str,
    company_name: str | None = None
) -> dict:
    """
    Execute Hybrid RAG pipeline.

    Parameters
    ----------
    question : str
        User question.

    company_name : str | None
        Optional company filter.

    Returns
    -------
    dict
    """

    # -----------------------------
    # Retrieval
    # -----------------------------

    start_time = time.perf_counter()

    context = build_hybrid_context(
        question=question,
        company_name=company_name
    )

    retrieval_time = (
        time.perf_counter() - start_time
    )

    documents = context["documents"]

    metadata = context["metadata"]

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

    prompt = build_hybrid_prompt(

        question=question,

        documents=documents,

        sentiment_text=sentiment_text,

        stock_text=stock_text

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

        "pipeline": "Hybrid RAG",

        "question": question,

        "company_name": company_name,

        "answer": answer,

        "documents": documents,

        "metadata": metadata,

        "graph_context": [],

        "sentiment": sentiment_data,

        "stock": stock_data,

        "retrieval_time": retrieval_time,

        "num_chunks": len(documents)

    }