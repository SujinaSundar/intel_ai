from app.rag.rag_pipeline import (
    ask_question
)


def main():

    company_name = "Infosys"

    while True:

        question = input(
            "\nAsk a question (type exit to quit): "
        )

        if question.lower() == "exit":

            break

        answer = ask_question(
            question=question,
            company_name=company_name
        )

        print("\nAnswer:\n")

        print(answer)


if __name__ == "__main__":

    main()