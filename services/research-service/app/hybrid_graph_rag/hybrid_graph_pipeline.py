"""
Hybrid GraphRAG Pipeline.
"""

from app.hybrid_graph_rag.hybrid_graph_context_builder import (
    build_hybrid_graph_context
)

from app.hybrid_graph_rag.hybrid_graph_prompt import (
    build_hybrid_graph_prompt
)

from app.llm.llm_service import (
    generate_answer
)


def ask_hybrid_graph_question(
    question: str,
    company_name: str
) -> str:
    """
    Hybrid GraphRAG pipeline.
    """

    context = build_hybrid_graph_context(
        question=question,
        company_name=company_name
    )

    sentiment_text = (
        str(context["sentiment"])
        if context["sentiment"]
        else "No sentiment found"
    )

    stock_text = (
        str(context["stock"])
        if context["stock"]
        else "No stock data found"
    )

    prompt = build_hybrid_graph_prompt(

        question=question,

        documents=
        context["documents"],

        graph_documents=
        context["graph_documents"],

        sentiment_text=
        sentiment_text,

        stock_text=
        stock_text
    )

    answer = generate_answer(
        prompt
    )

    return answer