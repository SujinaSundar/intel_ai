"""
Test Research Agent.
"""

from pprint import pprint

from app.agents.research_agent import (
    ResearchAgent
)


def main():
    """
    Test Research Agent.
    """

    agent = ResearchAgent()

    print()

    print("=" * 80)

    print(
        "Research Agent"
    )

    print("=" * 80)

    response = agent.answer(

        "Who is the CEO of Infosys?"

    )

    pprint(response)


if __name__ == "__main__":

    main()