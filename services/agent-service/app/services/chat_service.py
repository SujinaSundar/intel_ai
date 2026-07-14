"""
Chat Service.

Executes the LangGraph
workflow for frontend
requests.
"""

from app.langgraph.workflow import (
    WorkflowRunner
)


# ---------------------------------------------------------
# Workflow Runner
# ---------------------------------------------------------

workflow = WorkflowRunner()


# ---------------------------------------------------------
# Execute Workflow
# ---------------------------------------------------------

def ask_question(
    question: str
) -> str:
    """
    Execute the LangGraph
    workflow.

    Parameters
    ----------
    question : str
        User research question.

    Returns
    -------
    str
        Final response generated
        by the LangGraph workflow.
    """

    return workflow.run(

        question

    )