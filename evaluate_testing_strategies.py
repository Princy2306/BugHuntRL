
import csv

from testing_engine import TestingEngine
from sample_app import sample_target


STRATEGIES = {
    0: "Random Testing",
    1: "Boundary-Value Testing",
    2: "Input Mutation",
    3: "Sequence Generation",
}

RESULTS_FILE = "strategy_results.csv"
RUNS_PER_STRATEGY = 10


def evaluate_strategies():
    rows = []

    for strategy_id, strategy_name in STRATEGIES.items():
        for run_number in range(RUNS_PER_STRATEGY):
            # Use a fresh engine for a fair, independent run.
            engine = TestingEngine(
                target=sample_target,
                seed=42 + run_number,
            )

            report = engine.run(strategy=strategy_id)

            rows.append({
                "strategy_id": strategy_id,
                "strategy": strategy_name,
                "run": run_number + 1,
                "unique_bugs_found": len(report["new_bug_ids"]),
                "bug_ids": ";".join(report["new_bug_ids"]),
                "coverage_percent": report["coverage"],
                "tests_executed": report["tests_executed"],
                "target_calls_executed": report[
                    "target_calls_executed"
                ],
                "execution_cost": report["budget_cost"],
                "execution_time_seconds": report[
                    "execution_time_seconds"
                ],
            })

    with open(
        RESULTS_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results saved to {RESULTS_FILE}")
    print(f"Total runs: {len(rows)}")

    print("\nResults by strategy:")

    for strategy_id, strategy_name in STRATEGIES.items():
        strategy_rows = [
            row for row in rows
            if row["strategy_id"] == strategy_id
        ]

        average_bugs = sum(
            row["unique_bugs_found"] for row in strategy_rows
        ) / len(strategy_rows)

        average_coverage = sum(
            row["coverage_percent"] for row in strategy_rows
        ) / len(strategy_rows)

        print(
            f"{strategy_name}: "
            f"average bugs={average_bugs:.2f}, "
            f"average coverage={average_coverage:.2f}%"
        )


if __name__ == "__main__":
    evaluate_strategies()
