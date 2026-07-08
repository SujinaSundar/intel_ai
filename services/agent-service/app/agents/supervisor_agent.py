"""
Supervisor Agent.

Routes user requests
to the appropriate
domain-specific Agent.

The Supervisor Agent
uses an LLM to decide
which Agent should
handle a question.
"""

import json

from app.llm.llm_service import (
    generate_answer
)

from app.prompts.supervisor_prompt import (
    get_supervisor_prompt
)

from app.agents.finance_agent import (
    FinanceAgent
)

from app.agents.news_agent import (
    NewsAgent
)

from app.agents.research_agent import (
    ResearchAgent
)

from app.agents.comparison_agent import (
    ComparisonAgent
)

from app.agents.sector_agent import (
    SectorAgent
)


class SupervisorAgent:
    """
    Supervisor Agent.

    Uses an LLM to
    determine which
    Agent should
    answer a user's
    request.
    """

    def __init__(
        self
    ):
        """
        Initialize all
        domain Agents.
        """

        self.finance = FinanceAgent()

        self.news = NewsAgent()

        self.research = ResearchAgent()

        self.comparison = ComparisonAgent()

        self.sector = SectorAgent()

    # -----------------------------------------------------
    # Route Question
    # -----------------------------------------------------

    def route(
        self,
        question: str
    ) -> dict:
        """
        Route a question
        using the LLM.

        Parameters
        ----------
        question : str

        Returns
        -------
        dict
        """

        prompt = get_supervisor_prompt(
            question
        )

        response = generate_answer(
            prompt
        )

        try:

            decision = json.loads(
                response
            )

        except Exception:

            return {

                "error":

                    "Invalid routing response.",

                "response":

                    response

            }

        return decision
    # -----------------------------------------------------
    # Execute Request
    # -----------------------------------------------------

    def run(
        self,
        question: str
    ) -> dict:
        """
        Execute a user request.

        Parameters
        ----------
        question : str

        Returns
        -------
        dict
            Agent response.
        """

        decision = self.route(
            question
        )

        if "error" in decision:

            return decision

        agent = decision.get(
            "agent"
        )

        # -------------------------------------------------
        # Finance
        # -------------------------------------------------

        if agent == "Finance":

            return self.finance.answer(

                decision["company"]

            )

        # -------------------------------------------------
        # News
        # -------------------------------------------------

        if agent == "News":

            return self.news.answer(

                decision["company"]

            )

        # -------------------------------------------------
        # Research
        # -------------------------------------------------

        if agent == "Research":

            return self.research.answer(

                decision["question"]

            )

        # -------------------------------------------------
        # Comparison
        # -------------------------------------------------

        if agent == "Comparison":

            return self.comparison.compare(

                decision["company_one"],

                decision["company_two"]

            )

        # -------------------------------------------------
        # Sector
        # -------------------------------------------------

        if agent == "Sector":

            return self.sector.summarize(

                decision["sector"]

            )

        return {

            "error":

                "Unknown agent."

        }

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self
    ) -> dict:
        """
        Check all agents.

        Returns
        -------
        dict
        """

        return {

            "finance":

                self.finance.health_check(),

            "news":

                self.news.health_check(),

            "research":

                self.research.health_check(),

            "comparison":

                self.comparison.health_check(),

            "sector":

                self.sector.health_check()

        }
    # -----------------------------------------------------
    # Execute Request
    # -----------------------------------------------------

    def run(
        self,
        question: str
    ) -> str:
        """
        Execute a user request.

        Parameters
        ----------
        question : str

        Returns
        -------
        str
            Final response.
        """

        decision = self.route(
            question
        )

        if "error" in decision:

            return decision["error"]

        agent = decision.get(
            "agent"
        )

        result = None

        # -------------------------------------------------
        # Finance
        # -------------------------------------------------

        if agent == "Finance":

            result = self.finance.answer(

                decision["company"]

            )

        # -------------------------------------------------
        # News
        # -------------------------------------------------

        elif agent == "News":

            result = self.news.answer(

                decision["company"]

            )

        # -------------------------------------------------
        # Research
        # -------------------------------------------------

        elif agent == "Research":

            result = self.research.answer(

                decision["question"]

            )

        # -------------------------------------------------
        # Comparison
        # -------------------------------------------------

        elif agent == "Comparison":

            result = self.comparison.compare(

                decision["company_one"],

                decision["company_two"]

            )

        # -------------------------------------------------
        # Sector
        # -------------------------------------------------

        elif agent == "Sector":

            result = self.sector.summarize(

                decision["sector"]

            )

        else:

            return "Unknown agent selected."

        # -------------------------------------------------
        # Generate Final Response
        # -------------------------------------------------

        final_response = self.generator.generate(

            question,

            result

        )

        return final_response
    