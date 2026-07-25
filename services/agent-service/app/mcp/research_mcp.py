"""
Research MCP.

Provides research retrieval tools
for the Trading Research Agent.

This MCP communicates with the
Research Service through REST APIs.
"""

import logging
from typing import Any

import requests
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    RequestException,
    Timeout,
)

from app.database.config import settings
from app.exceptions.custom_exceptions import (
    InvalidRequestException,
    LLMServiceException,
)

logger = logging.getLogger(__name__)


class ResearchMCP:
    """
    Research MCP.

    Acts as a client for the
    Research Service.
    """

    BASE_URL = settings.RESEARCH_SERVICE_URL

    def answer_question(
        self,
        question: str,
    ) -> dict[str, Any]:
        """
        Answer a research question.

        Parameters
        ----------
        question : str
            User research question.

        Returns
        -------
        dict[str, Any]
            Hybrid GraphRAG response.

        Raises
        ------
        InvalidRequestException
            If the question is empty.

        LLMServiceException
            If the Research Service
            is unavailable or returns
            an unexpected response.
        """

        if not question or not question.strip():

            logger.warning(
                "Empty research question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        url = f"{self.BASE_URL}/research/ask"

        logger.info(
            "Calling Research Service | url=%s",
            url,
        )

        try:

            response = requests.post(
                url,
                json={
                    "question": question,
                },
                timeout=60,
            )

            response.raise_for_status()
            result = response.json()

            logger.info(
                "Research Service response:\n%s",
                result,
            )

            return result
            """logger.info(
                "Research Service responded successfully."
            )

            return response.json()"""

        except ConnectionError as error:

            logger.exception(
                "Unable to connect to Research Service."
            )

            raise LLMServiceException(
                "Research Service is not running."
            ) from error

        except Timeout as error:

            logger.exception(
                "Research Service request timed out."
            )

            raise LLMServiceException(
                "Research Service request timed out."
            ) from error

        except HTTPError as error:

            logger.exception(
                "Research Service returned HTTP %s.",
                response.status_code,
            )

            raise LLMServiceException(
                f"Research Service returned HTTP "
                f"{response.status_code}."
            ) from error

        except RequestException as error:

            logger.exception(
                "Unexpected request error."
            )

            raise LLMServiceException(
                "Failed to communicate with "
                "Research Service."
            ) from error

    def health_check(
        self,
    ) -> dict[str, Any]:
        """
        Check Research Service health.

        Returns
        -------
        dict[str, Any]
            Service health information.

        Raises
        ------
        LLMServiceException
            If the health endpoint
            cannot be reached.
        """

        url = f"{self.BASE_URL}/"

        logger.info(
            "Checking Research Service health."
        )

        try:

            response = requests.get(
                url,
                timeout=10,
            )

            response.raise_for_status()

            logger.info(
                "Research Service is healthy."
            )

            return response.json()

        except RequestException as error:

            logger.exception(
                "Research Service health check failed."
            )

            raise LLMServiceException(
                "Research Service is unavailable."
            ) from error


research_mcp = ResearchMCP()