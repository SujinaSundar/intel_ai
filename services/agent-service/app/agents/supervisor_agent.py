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
import logging
from typing import Any

from app.agents.comparison_agent import ComparisonAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.news_agent import NewsAgent
from app.agents.research_agent import ResearchAgent
from app.agents.sector_agent import SectorAgent
from app.exceptions.custom_exceptions import (
    InvalidRequestException,
    LLMServiceException,
)
from app.llm.llm_service import generate_answer
from app.prompts.supervisor_prompt import get_supervisor_prompt
from app.response.response_generator import ResponseGenerator
from app.utils.company_resolver import resolve_company

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Supervisor Agent.

    Uses an LLM to determine
    which domain Agent should
    answer a user's request.
    """

    def __init__(self) -> None:
        """
        Initialize all domain agents.
        """

        logger.info(
            "Initializing Supervisor Agent."
        )

        self.finance = FinanceAgent()
        self.news = NewsAgent()
        self.research = ResearchAgent()
        self.comparison = ComparisonAgent()
        self.sector = SectorAgent()
        self.generator = ResponseGenerator()

    # -----------------------------------------------------
    # Route Question
    # -----------------------------------------------------

    def route(
        self,
        question: str,
        history: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        """
        Route a question using the LLM.

        Parameters
        ----------
        question : str
            User question.

        history : list[dict[str, str]] | None
            Previous conversation history.

        Returns
        -------
        dict[str, Any]
            Parsed routing decision.

        Raises
        ------
        InvalidRequestException
            If the question is empty.

        LLMServiceException
            If routing fails.
        """

        if not question or not question.strip():

            logger.warning(
                "Empty question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        prompt = get_supervisor_prompt(
            question=question,
            history=history or [],
        )

        logger.info(
            "Routing question using Supervisor LLM."
        )

        logger.debug(
            "Supervisor Prompt:\n%s",
            prompt,
        )

        try:

            response = generate_answer(
                prompt
            )

            logger.info(
                "Supervisor raw response:\n%s",
                response,
            )

            decision = json.loads(
                response
            )
            # -------------------------------------------------
            # Recover missing company
            # -------------------------------------------------

            if (
                decision.get("agent")
                in (
                    "Finance",
                    "News",
                    "Sector",
                )
                and not decision.get("company")
            ):
                logger.info(
                    "Current question: %s",
                    question,
                )

                logger.info(
                    "Conversation history: %s",
                    history,
                )

                company = resolve_company(
                    question=question,
                    history=history or [],
                )

                if company:

                    logger.info(
                        "Recovered company from context: %s",
                        company,
                    )

                    decision["company"] = company

            logger.info(
                "Supervisor parsed decision: %s",
                decision,
            )

            logger.info(
                (
                    "Routing successful | "
                    "agent=%s | "
                    "company=%s | "
                    "sector=%s"
                ),
                decision.get("agent"),
                decision.get("company"),
                decision.get("sector"),
            )

            return decision

        except json.JSONDecodeError as error:

            logger.exception(
                "Failed to parse LLM routing response."
            )

            logger.error(
                "Invalid JSON returned by LLM:\n%s",
                response,
            )

            raise LLMServiceException(
                "Invalid routing response received from LLM."
            ) from error

        except Exception as error:

            logger.exception(
                "Supervisor routing failed."
            )

            raise LLMServiceException(
                "Unable to determine routing decision."
            ) from error

        # -------------------------------------------------
        # Finance
        # -------------------------------------------------

        if agent == "Finance":

            logger.info(
                "Routing to Finance Agent."
            )

            result = self.finance.answer(
                decision["company"]
            )

        # -------------------------------------------------
        # News
        # -------------------------------------------------

        elif agent == "News":

            logger.info(
                "Routing to News Agent."
            )

            result = self.news.answer(
                decision["company"]
            )

        # -------------------------------------------------
        # Research
        # -------------------------------------------------

        elif agent == "Research":

            logger.info(
                "Routing to Research Agent."
            )

            result = self.research.answer(
                decision["question"]
            )

        # -------------------------------------------------
        # Comparison
        # -------------------------------------------------

        elif agent == "Comparison":

            logger.info(
                "Routing to Comparison Agent."
            )

            result = self.comparison.answer(
                decision["company_one"],
                decision["company_two"],
            )

        # -------------------------------------------------
        # Sector
        # -------------------------------------------------

        elif agent == "Sector":

            logger.info(
                "Routing to Sector Agent."
            )

            result = self.sector.answer(
                decision["sector"]
            )

        else:

            logger.error(
                "Unknown agent received from LLM | agent=%s",
                agent,
            )

            raise LLMServiceException(
                f"Unknown agent '{agent}' selected."
            )

        logger.info(
            "Generating final response."
        )

        final_response = self.generator.generate(
            question,
            result,
        )

        logger.info(
            "Supervisor workflow completed successfully."
        )

        return final_response

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self,
    ) -> dict[str, Any]:
        """
        Check the health of all
        dependent agents.

        Returns
        -------
        dict[str, Any]
            Health status of all
            registered agents.
        """

        logger.info(
            "Running Supervisor health check."
        )

        return {
            "finance": self.finance.health_check(),
            "news": self.news.health_check(),
            "research": self.research.health_check(),
            "comparison": self.comparison.health_check(),
            "sector": self.sector.health_check(),
            "response_generator": (
                self.generator.health_check()
            ),
        }


supervisor_agent = SupervisorAgent()