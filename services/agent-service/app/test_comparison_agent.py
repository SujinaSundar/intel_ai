"""
Test Comparison Agent.
"""

from pprint import pprint

from app.agents.comparison_agent import (
    ComparisonAgent
)


def main():
    """
    Test Comparison Agent.
    """

    agent = ComparisonAgent()

    print()

    print("=" * 80)

    print(
        "Comparison Agent"
    )

    print("=" * 80)

    response = agent.compare(

        "Infosys",

        "TCS"

    )

    pprint(response)


if __name__ == "__main__":

    main()