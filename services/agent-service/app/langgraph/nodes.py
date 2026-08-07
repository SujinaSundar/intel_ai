"""
LangGraph Nodes.

Contains all workflow nodes
used by the LangGraph
orchestration.
"""

import logging

from app.agents.supervisor_agent import SupervisorAgent
from app.langgraph.state import AgentState
from app.response.response_generator import ResponseGenerator

logger = logging.getLogger(__name__)


class WorkflowNodes:
    """
    Workflow Nodes.

    Each node performs
    a single task and
    updates the shared
    workflow state.
    """

    def __init__(self) -> None:
        """
        Initialize workflow
        components.
        """

        logger.info(
            "Initializing workflow nodes."
        )

        self.supervisor = SupervisorAgent()
        self.generator = ResponseGenerator()

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    @staticmethod
    def _set_error(
        state: AgentState,
        message: str,
    ) -> AgentState:
        """
        Populate workflow state
        with an error response.
        """

        logger.error(message)

        state["agent_response"] = {
            "error": message
        }

        state["final_response"] = message

        return state

    # -----------------------------------------------------
    # Router Node
    # -----------------------------------------------------

    def router_node(
        self,
        state: AgentState,
    ) -> AgentState:
        """
        Route the user question
        using the Supervisor.
        """

        logger.info(
            "Executing router node."
        )

        route = self.supervisor.route(
            question=state["question"],
            history=state["history"],
        )

        logger.info(
            "Supervisor route: %s",
            route,
        )

        if not route or "error" in route:

            return self._set_error(
                state,
                (
                    route.get(
                        "error",
                        "Unable to determine the appropriate agent.",
                    )
                    if route
                    else "Supervisor returned no route."
                ),
            )

        state["route"] = route

        return state

    # -----------------------------------------------------
    # Finance Node
    # -----------------------------------------------------

    def finance_node(
        self,
        state: AgentState,
    ) -> AgentState:
        """
        Execute Finance Agent.
        """

        logger.info(
            "Executing finance node."
        )

        route = state["route"]

        company = route.get("company")

        if not company:

            return self._set_error(
                state,
                "Company name missing.",
            )

        state["agent_response"] = (
            self.supervisor.finance.answer(
                company_name=company,
                intent=route.get("intent"),
                trade_date=route.get("trade_date"),
                limit=route.get("limit"),
                question=state["question"],
            )
        )

        return state

    # -----------------------------------------------------
    # News Node
    # -----------------------------------------------------

    def news_node(
        self,
        state: AgentState,
    ) -> AgentState:
        """
        Execute News Agent.
        """

        logger.info(
            "Executing news node."
        )

        route = state["route"]

        company = route.get("company")

        if not company:

            return self._set_error(
                state,
                "Company name missing.",
            )

        state["agent_response"] = (
            self.supervisor.news.answer(
                question=state["question"],
                company_name=company,
            )
        )

        return state

    # -----------------------------------------------------
    # Research Node
    # -----------------------------------------------------

    def research_node(
        self,
        state: AgentState,
    ) -> AgentState:
        """
        Execute Research Agent.
        """

        logger.info(
            "Executing research node."
        )

        route = state["route"]

        question = route.get(
            "question",
            state["question"],
        )

        state["agent_response"] = (
            self.supervisor.research.answer(
                question
            )
        )

        logger.info(
            "Research node completed."
        )

        return state

    # -----------------------------------------------------
    # Comparison Node
    # -----------------------------------------------------

    def comparison_node(
        self,
        state: AgentState,
    ) -> AgentState:
        """
        Execute Comparison Agent.
        """

        logger.info(
            "Executing comparison node."
        )

        route = state["route"]

        company_one = route.get(
            "company_one"
        )

        company_two = route.get(
            "company_two"
        )

        # Validate company names
        if not company_one or not company_two:

            return self._set_error(
                state,
                "Comparison requires two company names.",
            )

        # Prevent comparing the same company
        if (
            company_one.strip().lower()
            == company_two.strip().lower()
        ):

            return self._set_error(
                state,
                "Please select two different companies for comparison.",
            )

        state["agent_response"] = (
            self.supervisor.comparison.answer(
                company_one,
                company_two,
            )
        )

        return state

     # -----------------------------------------------------
    # Sector Node
    # -----------------------------------------------------

    def sector_node(
        self,
        state: AgentState,
    ) -> AgentState:
        """
        Execute Sector Agent.
        """

        logger.info(
            "Executing sector node."
        )

        route = state["route"]

        sector = route.get(
            "sector"
        )

        company = route.get(
            "company"
        )

        question = route.get(
            "question",
            state["question"],
        )

        # At least one of sector or company must exist
        if not sector and not company:

            return self._set_error(
                state,
                "Sector or company information is missing.",
            )

        state["agent_response"] = (
            self.supervisor.sector.answer(
                question=question,
                sector=sector,
                company=company,
            )
        )

        return state

    # -----------------------------------------------------
    # Response Node
    # -----------------------------------------------------

    def response_node(
        self,
        state: AgentState,
    ) -> AgentState:
        """
        Generate the final
        natural language response.
        """

        logger.info(
            "Executing response node."
        )

        response_data = state["agent_response"]

        if (
            isinstance(response_data, dict)
            and "error" in response_data
        ):

            logger.warning(
                "Skipping response generation due to agent error."
            )

            state["final_response"] = (
                response_data["error"]
            )

            return state

        state["final_response"] = (
            self.generator.generate(
                question=state["question"],
                data=response_data,
            )
        )

        logger.info(
            "Response generation completed."
        )

        return state


workflow_nodes = WorkflowNodes()