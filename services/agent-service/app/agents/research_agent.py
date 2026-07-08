"""
Research Agent.

Handles research-related
questions for the Trading
Research Agent.

The Research Agent delegates
all retrieval tasks to the
Research MCP.
"""

from app.mcp.research_mcp import (
    ResearchMCP
)


class ResearchAgent:
    """
    Research Agent.

    Uses the Research MCP
    to answer questions
    from company reports.
    """

    def __init__(
        self
    ):
        """
        Initialize the
        Research Agent.
        """

        self.mcp = ResearchMCP()

    def answer(
        self,
        question: str
    ) -> dict:
        """
        Answer a research question.

        Parameters
        ----------
        question : str
            User research question.

        Returns
        -------
        dict
            Research Service response.
        """

        return self.mcp.answer_question(
            question
        )

    def health_check(
        self
    ) -> dict:
        """
        Check Research Service.

        Returns
        -------
        dict
            Service status.
        """

        return self.mcp.health_check()