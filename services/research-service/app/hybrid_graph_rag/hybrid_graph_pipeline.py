"""
Hybrid GraphRAG Pipeline.
"""

import time

from app.graph_rag.company_extractor import (
    extract_company
)

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
    question: str
) -> dict:
    """
    Execute Hybrid GraphRAG pipeline.

    Parameters
    ----------
    question : str

    Returns
    -------
    dict
    """

    # -----------------------------------
    # Company Extraction
    # -----------------------------------

    company_name = extract_company(
        question
    )

    if company_name is None:

        return {

            "pipeline": "Hybrid GraphRAG",

            "question": question,

            "company_name": None,

            "answer": "Company not found in question.",

            "documents": [],

            "metadata": [],

            "graph_context": [],

            "sentiment": None,

            "stock": None,

            "retrieval_time": 0.0,

            "num_chunks": 0,

            "num_triples": 0

        }

    # -----------------------------------
    # Hybrid Graph Retrieval
    # -----------------------------------

    start_time = time.perf_counter()

    context = build_hybrid_graph_context(

        question=question,

        company_name=company_name

    )

    retrieval_time = (

        time.perf_counter() - start_time

    )

    # -----------------------------------
    # Optional Context
    # -----------------------------------

    sentiment_text = (

        str(context["sentiment"])

        if context["sentiment"]

        else "No sentiment found."

    )

    stock_text = (

        str(context["stock"])

        if context["stock"]

        else "No stock data found."

    )

    # -----------------------------------
    # Prompt
    # -----------------------------------

    prompt = build_hybrid_graph_prompt(

        question=question,

        documents=context["documents"],

        graph_documents=context["graph_documents"],

        sentiment_text=sentiment_text,

        stock_text=stock_text

    )

    # -----------------------------------
    # LLM
    # -----------------------------------

    answer = generate_answer(
        prompt
    )

    # -----------------------------------
    # Return
    # -----------------------------------

    return {

        "pipeline": "Hybrid GraphRAG",

        "question": question,

        "company_name": company_name,

        "answer": answer,

        "documents": context["documents"],

        "metadata": context["metadata"],

        "graph_context": context["graph_documents"],

        "sentiment": context["sentiment"],

        "stock": context["stock"],

        "retrieval_time": retrieval_time,

        "num_chunks": len(
            context["documents"]
        ),

        "num_triples": len(
            context["graph_documents"]
        )

    }