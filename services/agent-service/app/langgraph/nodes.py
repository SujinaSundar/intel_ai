"""
LangGraph Nodes.

Contains all workflow nodes
used by the LangGraph
orchestration.
"""

from app.langgraph.state import AgentState

from app.agents.supervisor_agent import SupervisorAgent

from app.response.response_generator import ResponseGenerator


class WorkflowNodes:
    """
    Workflow Nodes.

    Each node performs
    a single task and
    updates the shared
    workflow state.
    """

    def __init__(self):
        """
        Initialize workflow
        components.
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
        Route the user
        question using
        the Supervisor.
        """

        route = self.supervisor.route(
            state["question"]
        )

        print("=" * 80)
        print("SUPERVISOR ROUTE")
        print(route)
        print("=" * 80)

        if not route or "error" in route:

            state["agent_response"] = {
                "error": route.get(
                    "error",
                    "Unable to determine the appropriate agent."
                ) if route else "Supervisor returned no route."
            }

            state["final_response"] = state["agent_response"]["error"]

            state["route"] = None

            return state

        state["route"] = route

        return state
       # -----------------------------------------------------
    # Finance Node
    # -----------------------------------------------------

    def finance_node(
        self,
        state: AgentState
    ) -> AgentState:
        """
        Execute Finance Agent.
        """

        route = state["route"]

        company = route.get("company")

        if not company:

            state["agent_response"] = {
                "error": "Company name missing."
            }

            return state

        state["agent_response"] = self.supervisor.finance.answer(
            company_name=company,
            intent=route.get("intent"),
            trade_date=route.get("trade_date"),
            limit=route.get("limit"),
            question=state["question"],
        )

        return state

    # -----------------------------------------------------
    # News Node
    # -----------------------------------------------------

    def news_node(
        self,
        state: AgentState
    ) -> AgentState:
        """
        Execute News Agent.
        """

        route = state["route"]

        company = route.get("company")

        if not company:

            state["agent_response"] = {
                "error": "Company name missing."
            }

            return state

        state["agent_response"] = self.supervisor.news.answer(
            question=state["question"],
            company_name=company,
        )

        return state

    # -----------------------------------------------------
    # Research Node
    # -----------------------------------------------------

    def research_node(
    self,
    state: AgentState
    ) -> AgentState:

        print("=" * 80)
        print("INSIDE RESEARCH NODE")
        print("Question:", state["question"])
        print("=" * 80)

        route = state["route"]

        question = route.get(
            "question",
            state["question"]
        )

        state["agent_response"] = self.supervisor.research.answer(question)

        print("Research Response:", state["agent_response"])

        return state

    # -----------------------------------------------------
    # Comparison Node
    # -----------------------------------------------------

    def comparison_node(
        self,
        state: AgentState
    ) -> AgentState:
        """
        Execute Comparison Agent.
        """

        route = state["route"]

        company_one = route.get("company_one")
        company_two = route.get("company_two")

        if not company_one or not company_two:

            state["agent_response"] = {
                "error": "Comparison requires two company names."
            }

            return state

        state["agent_response"] = self.supervisor.comparison.answer(
            company_one,
            company_two,
        )

        return state

    # -----------------------------------------------------
    # Sector Node
    # -----------------------------------------------------

    def sector_node(
        self,
        state: AgentState
    ) -> AgentState:
        """
        Execute Sector Agent.
        """

        route = state["route"]

        sector = route.get("sector")

        question = route.get(
            "question",
            state["question"]
        )

        if not sector:

            state["agent_response"] = {
                "error": "Sector name missing."
            }

            return state

        state["agent_response"] = self.supervisor.sector.answer(
            question=question,
            sector=sector,
        )

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
        response.
        """

        response_data = state["agent_response"]

        if isinstance(response_data, dict) and "error" in response_data:

            state["final_response"] = response_data["error"]

            return state

        response = self.generator.generate(
            question=state["question"],
            data=response_data,
        )

        state["final_response"] = response

        return state
