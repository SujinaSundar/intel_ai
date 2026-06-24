"""
Hybrid RAG pipeline.
"""

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
    company_name: str
) -> str:
    """
    Answer user question using Hybrid RAG.
    """

    context = build_hybrid_context(

        question=question,

        company_name=company_name
    )

    prompt = build_hybrid_prompt(

        question=question,

        documents=context["documents"],

        sentiment_text=context["sentiment"],

        stock_text=context["stock"]
    )

    response = generate_answer(
        prompt
    )

    return response