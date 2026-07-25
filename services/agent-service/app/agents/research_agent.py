"""
Research Agent.

Handles research-related
questions for the Trading
Research Agent.

The Research Agent delegates
all retrieval tasks to the
Research MCP.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.mcp.research_mcp import ResearchMCP

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Research Agent.

    Uses the Research MCP
    to answer questions
    from company reports.
    """

    def __init__(self) -> None:
        """
        Initialize the
        Research MCP.
        """

        logger.info(
            "Initializing Research Agent."
        )

        self.mcp = ResearchMCP()

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------

    def answer(
        self,
        question: str,
    ) -> dict[str, Any]:
        """
        Answer a research question.

        Parameters
        ----------
        question : str
            User research question.

        Returns
        -------
        dict[str, Any]
            Research response.

        Raises
        ------
        InvalidRequestException
            If the question is empty.
        """

        if not question or not question.strip():

            logger.warning(
                "Empty research question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        logger.info(
            "Processing research request."
        )

        return self.mcp.answer_question(
            question
        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self,
    ) -> dict[str, Any]:
        """
        Check Research MCP health.

        Returns
        -------
        dict[str, Any]
            Research MCP health status.
        """

        logger.info(
            "Research Agent health check."
        )

        return self.mcp.health_check()


research_agent = ResearchAgent()