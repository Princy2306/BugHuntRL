
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
RUNS_PER_STRATEGY = 20
INITIAL_BUDGET = 100


def evaluate_strategies():
    rows = []

    for strategy_id, strategy_name in STRATEGIES.items():
        for run_number in range(RUNS_PER_STRATEGY):
            engine = TestingEngine(
                target=sample_target,
                seed=42 + run_number,
            )

            remaining_budget = INITIAL_BUDGET
            discovered_bugs = set()
            covered_lines = set()
            total_statement_lines = 0
            tests_executed = 0
            target_calls = 0
            total_time = 0.0
            actions = 0

            while remaining_budget >= TestingEngine.STRATEGY_COSTS[strategy_id]:
                report = engine.run(
                    strategy=strategy_id,
                    budget=remaining_budget,
                )

                discovered_bugs.update(report["new_bug_ids"])
                covered_lines.update(report["executed_statement_lines"])
                total_statement_lines = report["total_statement_lines"]

                tests_executed += report["tests_executed"]
                target_calls += report["target_calls_executed"]
                total_time += report["execution_time_seconds"]
                remaining_budget -= report["budget_cost"]
                actions += 1

            coverage_percent = (
                100.0 * len(covered_lines) / total_statement_lines
                if total_statement_lines
                else 0.0
            )

            rows.append({
                "strategy_id": strategy_id,
                "strategy": strategy_name,
                "run": run_number + 1,
                "unique_bugs_found": len(discovered_bugs),
                "bug_ids": ";".join(sorted(discovered_bugs)),
                "coverage_percent": round(coverage_percent, 2),
                "tests_executed": tests_executed,
                "target_calls_executed": target_calls,
                "actions": actions,
                "initial_budget": INITIAL_BUDGET,
                "budget_used": INITIAL_BUDGET - remaining_budget,
                "budget_remaining": remaining_budget,
                "execution_time_seconds": round(total_time, 6),
            })

    with open(
        RESULTS_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
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

        average_budget = sum(
            row["budget_used"] for row in strategy_rows
        ) / len(strategy_rows)

        print(
            f"{strategy_name}: "
            f"average bugs={average_bugs:.2f}, "
            f"average coverage={average_coverage:.2f}%, "
            f"average budget used={average_budget:.2f}"
        )


if __name__ == "__main__":
    evaluate_strategies()
