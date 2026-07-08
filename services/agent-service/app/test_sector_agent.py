"""
Test Sector Agent.
"""

from pprint import pprint

from app.agents.sector_agent import (
    SectorAgent
)


def main():
    """
    Test Sector Agent.
    """

    agent = SectorAgent()

    print()

    print("=" * 80)

    print(
        "Sector Agent"
    )

    print("=" * 80)

    response = agent.summarize(
        "Banking"
    )

    pprint(response)


if __name__ == "__main__":

    main()