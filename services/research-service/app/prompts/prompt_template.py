"""
Prompt template for RAG.
"""


def build_prompt(
    question: str,
    documents: list[str],
    sentiment: str,
    stock_data: str
) -> str:
    """
    Build prompt for LLM.

    Parameters
    ----------
    question : str

    documents : list[str]

    sentiment : str

    stock_data : str

    Returns
    -------
    str
    """

    report_context = "\n\n".join(
        documents
    )

    prompt = f"""
You are a financial research assistant.

Answer ONLY using the provided context.

If the answer is not present, say:
"I don't have enough information."

REPORT CONTEXT:
{report_context}

NEWS SENTIMENT:
{sentiment}

STOCK DATA:
{stock_data}

QUESTION:
{question}
"""

    return prompt