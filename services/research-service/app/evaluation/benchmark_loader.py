"""
Benchmark loader.
"""

import json

from pathlib import Path


def load_benchmark() -> list[dict]:
    """
    Load benchmark dataset.

    Returns
    -------
    list[dict]
    """

    benchmark_path = (
        Path(__file__).parent
        / "benchmark.json"
    )

    with open(
        benchmark_path,
        "r",
        encoding="utf-8"
    ) as file:

        benchmark = json.load(file)

    print(
        f"Loaded {len(benchmark)} benchmark questions."
    )

    return benchmark