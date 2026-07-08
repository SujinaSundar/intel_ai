"""
Graph RAG pipeline.
"""

import time

from app.graph_rag.graph_context_builder import (
    build_graph_context
)

from app.graph_rag.graph_prompt_template import (
    build_graph_prompt
)

from app.graph_rag.company_extractor import (
    extract_company
)

from app.llm.llm_service import (
    generate_answer
)


def ask_graph_question(
    question: str,
    company_name: str | None = None
) -> dict:
    """
    Execute Graph RAG pipeline.

    Parameters
    ----------
    question : str

    company_name : str | None
        Optional company filter.

    Returns
    -------
    dict
    """

    # -----------------------------------
    # Extract company automatically
    # -----------------------------------

    if company_name is None:

        company_name = extract_company(
            question
        )

    if company_name is None:

        return {

            "pipeline": "Graph RAG",

            "question": question,

            "company_name": None,

            "answer": "Company not found.",

            "documents": [],

            "metadata": [],

            "graph_context": [],

            "sentiment": None,

            "stock": None,

            "retrieval_time": 0.0,

            "num_chunks": 0

        }

    # -----------------------------------
    # Graph Retrieval
    # -----------------------------------

    start_time = time.perf_counter()

    context = build_graph_context(

    question=question,

    company_name=company_name

)

    retrieval_time = (
        time.perf_counter() - start_time
    )

    graph_documents = context[
        "graph_documents"
    ]

    # -----------------------------------
    # Prompt
    # -----------------------------------

    prompt = build_graph_prompt(

        question=question,

        graph_documents=graph_documents

    )

    # -----------------------------------
    # LLM
    # -----------------------------------
    print()
    print("=" * 100)
    print("PROMPT")
    print("=" * 100)
    print(prompt)
    print("=" * 100)
    answer = generate_answer(
        prompt
    )

    # -----------------------------------
    # Return
    # -----------------------------------

    return {

        "pipeline": "Graph RAG",

        "question": question,

        "company_name": company_name,

        "answer": answer,

        # Use graph triples as documents
        # so the evaluation framework works
        "documents": graph_documents,

        "metadata": [],

        "graph_context": graph_documents,

        "sentiment": None,

        "stock": None,

        "retrieval_time": retrieval_time,

        "num_chunks": len(graph_documents)

    }