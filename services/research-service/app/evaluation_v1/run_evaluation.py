"""
Run complete evaluation.
"""

from app.evaluation.evaluator import (
    evaluate_all
)

from app.evaluation.report_generator import (
    print_report
)


def main():

    results = evaluate_all()

    print_report(results)


if __name__ == "__main__":

    main()