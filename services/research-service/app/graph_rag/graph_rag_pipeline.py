"""
GraphRAG pipeline.
"""

from app.graph_rag.graph_context_builder import (
    build_graph_context
)

from app.graph_rag.graph_prompt_template import (
    build_graph_prompt
)

from app.llm.llm_service import (
    generate_answer
)


def ask_graph_question(
    question: str,
    company_name: str
) -> str:
    """
    Answer question using GraphRAG.
    """

    context = build_graph_context(
        company_name
    )

    prompt = build_graph_prompt(

        question=question,

        graph_documents=
        context["graph_documents"],

        sentiment_text=
        context["sentiment"],

        stock_text=
        context["stock"]
    )

    answer = generate_answer(
        prompt
    )

    return answer