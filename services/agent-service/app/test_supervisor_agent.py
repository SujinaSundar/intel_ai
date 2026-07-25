"""
Test Supervisor Agent.
"""

from pprint import pprint

from app.agents.supervisor_agent import SupervisorAgent


def main():
    """
    Test Supervisor Agent.
    """

    agent = SupervisorAgent()

    print()

    print("=" * 80)

    print(
        "Supervisor Agent"
    )

    print("=" * 80)

    while True:

        question = input(

            "\nAsk a question (exit to quit): "

        )

        if question.lower() == "exit":

            break

        response = agent.run(
            question
        )

        print()

        pprint(response)


if __name__ == "__main__":

    main()