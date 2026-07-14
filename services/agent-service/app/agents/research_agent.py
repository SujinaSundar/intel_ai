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
        Research MCP.
        """

        self.mcp = ResearchMCP()

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------

    def answer(
        self,
        question: str
    ) -> dict:
        """
        Default response.

        Answers a research
        question using the
        Research MCP.

        Parameters
        ----------
        question : str

        Returns
        -------
        dict
        """

        return self.mcp.answer_question(
            question
        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self
    ) -> dict:
        """
        Check Research MCP.

        Returns
        -------
        dict
        """

        return self.mcp.health_check()