"""
Global GraphRAG Pipeline.
"""

from app.graph_rag.global_graph_context_builder import (
    build_global_graph_context
)

from app.graph_rag.graph_prompt_template import (
    build_graph_prompt
)

from app.llm.llm_service import (
    generate_answer
)


def ask_global_graph_question(
    question: str
) -> str:
    """
    Answer graph-wide questions.
    """

    context = (
        build_global_graph_context()
    )

    graph_documents = (
        context["graph_documents"]
    )

    """print()

    print("=" * 80)
    print("GLOBAL GRAPH CONTEXT")
    print("=" * 80)

    for doc in graph_documents[:20]:

        print(doc)
"""
    prompt = build_graph_prompt(

        question=question,

        graph_documents=
        graph_documents
    )

    answer = generate_answer(
        prompt
    )

    return answer