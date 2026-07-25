"""
Workflow Runner.

Provides a simple wrapper
around the LangGraph
workflow.
"""

import logging

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.langgraph.graph import (
    AgentWorkflow,
)

logger = logging.getLogger(__name__)


class WorkflowRunner:
    """
    Workflow Runner.

    Executes the complete
    LangGraph workflow.
    """

    def __init__(self) -> None:
        """
        Initialize the
        LangGraph workflow.
        """

        logger.info(
            "Initializing Workflow Runner."
        )

        self.workflow = AgentWorkflow()

    def run(
        self,
        question: str,
    ) -> str:
        """
        Execute the LangGraph
        workflow.

        Parameters
        ----------
        question : str
            User question.

        Returns
        -------
        str
            Final response generated
            by the workflow.

        Raises
        ------
        InvalidRequestException
            If the question is empty.
        """

        if not question or not question.strip():

            logger.warning(
                "Empty workflow question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        logger.info(
            "Executing workflow."
        )

        response = self.workflow.run(
            question
        )

        logger.info(
            "Workflow completed successfully."
        )

        return response

    def health_check(
        self,
    ) -> dict[str, str]:
        """
        Check Workflow Runner
        health status.

        Returns
        -------
        dict[str, str]
            Workflow status.
        """

        logger.info(
            "Workflow Runner health check."
        )

        return {
            "workflow_runner": "Available"
        }


workflow_runner = WorkflowRunner()