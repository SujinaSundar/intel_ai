"""
LangGraph Workflow.

Builds the Agentic AI
workflow using LangGraph.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
    LLMServiceException,
)
from app.langgraph.nodes import WorkflowNodes
from app.langgraph.state import AgentState
from langgraph.graph import END, StateGraph

logger = logging.getLogger(__name__)

ROUTE_MAPPING = {
    "Finance": "finance",
    "News": "news",
    "Research": "research",
    "Comparison": "comparison",
    "Sector": "sector",
}


class AgentWorkflow:
    """
    LangGraph Workflow.

    Builds the execution
    graph for the Trading
    Research Agent.
    """

    def __init__(self) -> None:
        """
        Initialize and compile
        the workflow graph.
        """

        logger.info(
            "Initializing LangGraph workflow."
        )

        self.nodes = WorkflowNodes()
        self.builder = StateGraph(AgentState)

        self._build()

    # -----------------------------------------------------
    # Route Decision
    # -----------------------------------------------------

    def _route(
        self,
        state: AgentState,
    ) -> str:
        """
        Decide the next
        LangGraph node.

        Parameters
        ----------
        state : AgentState

        Returns
        -------
        str
            Next workflow node.
        """

        route = state.get("route")

        logger.info(
            "Evaluating workflow route."
        )

        if route is None:

            logger.error(
                "Route information is missing."
            )

            return END

        agent = route.get("agent")

        logger.info(
            "Selected agent: %s",
            agent,
        )

        next_node = ROUTE_MAPPING.get(agent)

        if next_node is None:

            logger.error(
                "Unknown agent received: %s",
                agent,
            )

            return END

        return next_node

    # -----------------------------------------------------
    # Build Workflow
    # -----------------------------------------------------

    def _build(
        self,
    ) -> None:
        """
        Build and compile
        the LangGraph workflow.
        """

        logger.info(
            "Building LangGraph workflow."
        )

        self.builder.add_node(
            "router",
            self.nodes.router_node,
        )

        self.builder.add_node(
            "finance",
            self.nodes.finance_node,
        )

        self.builder.add_node(
            "news",
            self.nodes.news_node,
        )

        self.builder.add_node(
            "research",
            self.nodes.research_node,
        )

        self.builder.add_node(
            "comparison",
            self.nodes.comparison_node,
        )

        self.builder.add_node(
            "sector",
            self.nodes.sector_node,
        )

        self.builder.add_node(
            "response",
            self.nodes.response_node,
        )

        self.builder.set_entry_point(
            "router"
        )

        self.builder.add_conditional_edges(
            "router",
            self._route,
            {
                "finance": "finance",
                "news": "news",
                "research": "research",
                "comparison": "comparison",
                "sector": "sector",
                END: END,
            },
        )

        self.builder.add_edge(
            "finance",
            "response",
        )

        self.builder.add_edge(
            "news",
            "response",
        )

        self.builder.add_edge(
            "research",
            "response",
        )

        self.builder.add_edge(
            "comparison",
            "response",
        )

        self.builder.add_edge(
            "sector",
            "response",
        )

        self.builder.add_edge(
            "response",
            END,
        )

        self.graph = self.builder.compile()

        logger.info(
            "LangGraph workflow compiled successfully."
        )

    # -----------------------------------------------------
    # Run Workflow
    # -----------------------------------------------------

    def run(
        self,
        question: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Execute the LangGraph
        workflow.

        Parameters
        ----------
        question : str

        history : list[dict[str, str]] | None
            Previous conversation
            history.

        Returns
        -------
        str
            Final response.
        """

        if not question or not question.strip():

            logger.warning(
                "Empty workflow question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        logger.info(
            "Executing LangGraph workflow."
        )

        state: dict[str, Any] = {
            "question": question,
            "history": history or [],
            "route": None,
            "agent_response": None,
            "final_response": None,
        }

        result = self.graph.invoke(
            state
        )

        response = result.get(
            "final_response"
        )

        if not response:

            logger.error(
                "Workflow completed without a final response."
            )

            raise LLMServiceException(
                "Workflow failed to generate a response."
            )

        logger.info(
            "Workflow execution completed successfully."
        )

        return response


agent_workflow = AgentWorkflow()