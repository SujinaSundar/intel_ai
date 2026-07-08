"""
Workflow Runner.

Provides a simple wrapper
around the LangGraph
workflow.
"""

from app.langgraph.graph import (
    AgentWorkflow
)


class WorkflowRunner:
    """
    Workflow Runner.

    Executes the complete
    LangGraph workflow.
    """

    def __init__(
        self
    ):
        """
        Initialize workflow.
        """

        self.workflow = AgentWorkflow()

    def run(
        self,
        question: str
    ) -> str:
        """
        Execute workflow.

        Parameters
        ----------
        question : str

        Returns
        -------
        str
        """

        return self.workflow.run(
            question
        )