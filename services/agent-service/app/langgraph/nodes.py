"""
LangGraph Nodes.

Contains all workflow nodes
used by the LangGraph
orchestration.
"""

from app.langgraph.state import (
    AgentState
)

from app.agents.supervisor_agent import (
    SupervisorAgent
)

from app.response.response_generator import (
    ResponseGenerator
)


class WorkflowNodes:
    """
    Workflow Nodes.

    Each node updates
    the shared state.
    """

    def __init__(
        self
    ):
        """
        Initialize components.
        """

        self.supervisor = SupervisorAgent()

        self.generator = ResponseGenerator()

    # -----------------------------------------------------
    # Router Node
    # -----------------------------------------------------

    def router_node(
        self,
        state: AgentState
    ) -> AgentState:
        """
        Decide which Agent
        should handle the
        question.
        """

        route = self.supervisor.route(

            state["question"]

        )

        state["route"] = route

        return state
        # -----------------------------------------------------
    # Agent Node
    # -----------------------------------------------------

    def agent_node(
        self,
        state: AgentState
    ) -> AgentState:
        """
        Execute the selected
        Agent.
        """

        route = state["route"]

        if route is None:

            state["agent_response"] = {

                "error":

                    "Routing failed."

            }

            return state

        agent = route.get(
            "agent"
        )

        if agent == "Finance":

            result = self.supervisor.finance.answer(

                route["company"]

            )

        elif agent == "News":

            result = self.supervisor.news.answer(

                route["company"]

            )

        elif agent == "Research":

            result = self.supervisor.research.answer(

                route["question"]

            )

        elif agent == "Comparison":

            result = self.supervisor.comparison.compare(

                route["company_one"],

                route["company_two"]

            )

        elif agent == "Sector":

            result = self.supervisor.sector.summarize(

                route["sector"]

            )

        else:

            result = {

                "error":

                    "Unknown agent."

            }

        state["agent_response"] = result

        return state

    # -----------------------------------------------------
    # Response Node
    # -----------------------------------------------------

    def response_node(
        self,
        state: AgentState
    ) -> AgentState:
        """
        Generate the final
        natural language
        response.
        """

        response = self.generator.generate(

            question=state["question"],

            data=state["agent_response"]

        )

        state["final_response"] = response

        return state