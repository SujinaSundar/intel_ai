"""
Evaluate Traditional RAG.
"""

from app.rag.rag_pipeline import (
    ask_question
)

TEST_CASES = [

    {
        "company": "HDFC Bank",
        "question": "What does HDFC Bank focus on?",
        "expected": "Banking"
    },

    {
        "company": "Reliance Industries",
        "question": "What industries does Reliance Industries focus on?",
        "expected": "Energy"
    },

    {
        "company": "HDFC Bank",
        "question": "What policies are associated with HDFC Bank?",
        "expected": "Information Security Policy"
    },

    {
        "company": "HDFC Bank",
        "question": "Which companies focus on Banking?",
        "expected": "HDFC Bank"
    },

    {
        "company": "HDFC Bank",
        "question": "Which companies have acquisitions?",
        "expected": "HDFC Bank"
    },

    {
        "company": "HDFC Bank",
        "question": "Compare HDFC Bank and Reliance Industries.",
        "expected": "Banking"
    },

    {
        "company": "Reliance Industries",
        "question": "Which companies focus on more than one industry?",
        "expected": "Reliance Industries"
    }

]


def evaluate():

    correct = 0

    total = len(TEST_CASES)

    print()
    print("=" * 80)
    print("RAG EVALUATION")
    print("=" * 80)

    for test in TEST_CASES:

        answer = ask_question(

            question=test["question"],

            company_name=test["company"]
        )

        expected = test["expected"]

        passed = (
            expected.lower()
            in answer.lower()
        )

        if passed:

            correct += 1

        print()
        print("=" * 80)

        print(
            test["question"]
        )

        print()

        print(
            "Expected:",
            expected
        )

        print()

        print(
            "Answer:",
            answer
        )

        print()

        print(
            "PASS"
            if passed
            else
            "FAIL"
        )

    accuracy = (
        correct / total
    ) * 100

    print()
    print("=" * 80)

    print(
        f"Accuracy: {accuracy:.2f}%"
    )

    print("=" * 80)


if __name__ == "__main__":

    evaluate()