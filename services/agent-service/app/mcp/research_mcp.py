"""
Research MCP.

Provides research retrieval tools
for the Trading Research Agent.

This MCP communicates with the
Research Service through REST APIs.
"""

import requests
from app.database.config import settings


class ResearchMCP:
    """
    Research MCP.

    Acts as a client for the
    Research Service.
    """

    BASE_URL = settings.RESEARCH_SERVICE_URL

    def answer_question(
        self,
        question: str
    ) -> dict:
        """
        Answer a research question.

        Parameters
        ----------
        question : str
            User research question.

        Returns
        -------
        dict
            Hybrid GraphRAG response.
        """

        try:

            response = requests.post(

                f"{self.BASE_URL}/research/ask",

                json={
                    "question": question
                },

                timeout=60

            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.ConnectionError:

            return {

                "error":
                    "Research Service is not running."

            }

        except requests.exceptions.HTTPError:

            return {

                "error":
                    f"HTTP Error: {response.status_code}"

            }

        except Exception as error:

            return {

                "error":
                    str(error)

            }

    def health_check(
        self
    ) -> dict:
        """
        Check Research Service status.

        Returns
        -------
        dict
            Service health.
        """

        try:

            response = requests.get(

                f"{self.BASE_URL}/"

            )

            response.raise_for_status()

            return response.json()

        except Exception:

            return {

                "status": "Unavailable"

            }