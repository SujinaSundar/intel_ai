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
    # Route Decision
    # -----------------------------------------------------

    def _route(
        self,
        state: AgentState
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
        """

        route = state["route"]

        if route is None:

            return END

        agent = route.get(
            "agent"
        )

        if agent == "Finance":

            return "finance"

        elif agent == "News":

            return "news"

        elif agent == "Research":

            return "research"

        elif agent == "Comparison":

            return "comparison"

        elif agent == "Sector":

            return "sector"

        return END
        # -----------------------------------------------------
    # Build Workflow
    # -----------------------------------------------------

    def _build(
        self
    ):
        """
        Build the LangGraph
        workflow.
        """

        # -------------------------------------------------
        # Add Nodes
        # -------------------------------------------------

        self.builder.add_node(

            "router",

            self.nodes.router_node

        )

        self.builder.add_node(

            "finance",

            self.nodes.finance_node

        )

        self.builder.add_node(

            "news",

            self.nodes.news_node

        )

        self.builder.add_node(

            "research",

            self.nodes.research_node

        )

        self.builder.add_node(

            "comparison",

            self.nodes.comparison_node

        )

        self.builder.add_node(

            "sector",

            self.nodes.sector_node

        )

        self.builder.add_node(

            "response",

            self.nodes.response_node

        )

        # -------------------------------------------------
        # Entry Point
        # -------------------------------------------------

        self.builder.set_entry_point(

            "router"

        )

        # -------------------------------------------------
        # Conditional Routing
        # -------------------------------------------------

        self.builder.add_conditional_edges(

            "router",

            self._route,

            {

                "finance": "finance",

                "news": "news",

                "research": "research",

                "comparison": "comparison",

                "sector": "sector"

            }

        )

        # -------------------------------------------------
        # Response Edges
        # -------------------------------------------------

        self.builder.add_edge(

            "finance",

            "response"

        )

        self.builder.add_edge(

            "news",

            "response"

        )

        self.builder.add_edge(

            "research",

            "response"

        )

        self.builder.add_edge(

            "comparison",

            "response"

        )

        self.builder.add_edge(

            "sector",

            "response"

        )

        self.builder.add_edge(

            "response",

            END

        )

        # -------------------------------------------------
        # Compile
        # -------------------------------------------------

        self.graph = self.builder.compile()
        # -----------------------------------------------------
    # Run Workflow
    # -----------------------------------------------------

    def run(
        self,
        question: str
    ) -> str:
        """
        Execute the LangGraph
        workflow.

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