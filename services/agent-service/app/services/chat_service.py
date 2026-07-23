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
    question: str,
    user_id: int,
):
    """
    Execute the LangGraph
    workflow.

    Parameters
    ----------
    question : str
        User research question.

    user_id : int
        Authenticated user ID.

    Returns
    -------
    str
        Final response generated
        by the LangGraph workflow.
    """

    print(f"Executing workflow for User ID: {user_id}")

    return workflow.run(question)