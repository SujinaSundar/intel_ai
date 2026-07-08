"""
LangGraph Workflow.

Builds the Agentic AI
workflow using LangGraph.
"""

from langgraph.graph import (
    StateGraph,
    END
)

from app.langgraph.state import (
    AgentState
)

from app.langgraph.nodes import (
    WorkflowNodes
)


class AgentWorkflow:
    """
    LangGraph Workflow.

    Builds the execution
    graph for the Trading
    Research Agent.
    """

    def __init__(
        self
    ):
        """
        Initialize workflow.
        """

        self.nodes = WorkflowNodes()

        self.builder = StateGraph(
            AgentState
        )

        self._build()

    # -----------------------------------------------------
    # Build Workflow
    # -----------------------------------------------------

    def _build(
        self
    ):
        """
        Build LangGraph.
        """

        # -----------------------------
        # Add Nodes
        # -----------------------------

        self.builder.add_node(

            "router",

            self.nodes.router_node

        )

        self.builder.add_node(

            "agent",

            self.nodes.agent_node

        )

        self.builder.add_node(

            "response",

            self.nodes.response_node

        )

        # -----------------------------
        # Entry Point
        # -----------------------------

        self.builder.set_entry_point(

            "router"

        )

        # -----------------------------
        # Edges
        # -----------------------------

        self.builder.add_edge(

            "router",

            "agent"

        )

        self.builder.add_edge(

            "agent",

            "response"

        )

        self.builder.add_edge(

            "response",

            END

        )

        # -----------------------------
        # Compile
        # -----------------------------

        self.graph = self.builder.compile()

    # -----------------------------------------------------
    # Run Workflow
    # -----------------------------------------------------

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

        state = {

            "question": question,

            "route": None,

            "agent_response": None,

            "final_response": None

        }

        result = self.graph.invoke(

            state

        )

        return result[
            "final_response"
        ]