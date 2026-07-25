"""
Run evaluation.
"""

from app.evaluation.evaluator import evaluate_all
from app.evaluation.report_generator import print_report
from app.evaluation.visualization import plot_results


def main() -> None:
    """
    Execute evaluation pipeline.
    """

    results = evaluate_all()

    print_report(
        results
    )

    plot_results()


if __name__ == "__main__":

    main()