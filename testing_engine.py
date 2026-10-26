
import random
import time
import inspect
from typing import Any, Callable

from coverage import Coverage


class TestingEngine:
    """Run testing strategies and measure target code coverage."""

    __test__ = False

    STRATEGY_COSTS = {
        0: 5,   # Random testing
        1: 8,   # Boundary-value testing
        2: 6,   # Input mutation
        3: 10,  # Sequence generation
    }

    def __init__(
        self,
        target: Callable[..., Any],
        seed: int = 42,
        bug_detector: Callable[[Any], list[str]] | None = None,
    ):
        self.target = target
        self.rng = random.Random(seed)
        self.bug_detector = (
            bug_detector or self._default_bug_detector
        )
        self.seen_bugs: set[str] = set()

    @staticmethod
    def _default_bug_detector(result: Any) -> list[str]:
        """Extract bug IDs from a structured target result."""
        if isinstance(result, dict):
            return list(result.get("bug_ids", []))
        return []

    def run(self, strategy: int, budget: int = 100) -> dict:
        """Execute a strategy and return its testing report."""

        if strategy not in self.STRATEGY_COSTS:
            raise ValueError("Strategy must be between 0 and 3.")

        cost = self.STRATEGY_COSTS[strategy]

        if budget < cost:
            raise ValueError("Insufficient budget for this strategy.")

        started = time.perf_counter()
        cases = self._generate_cases(strategy)

        results = []
        newly_seen = set()

        # Identify the Python module containing the target.
        target_module = inspect.getmodule(self.target)
        target_file = inspect.getsourcefile(self.target)

        if target_module is None or target_file is None:
            raise ValueError(
                "The target must be a Python function in a source file."
            )

        # Measure only the target's module, not this engine.
        cov = Coverage(
            source=[target_module.__name__],
            branch=True,
            data_file=None,
        )

        cov.start()

        try:
            for case in cases:
                try:
                    # Execute the selected testing strategy.
                    if strategy == 3:
                        sequence_results = self._execute_sequence(case)
                    else:
                        sequence_results = [self.target(*case)]

                    case_bug_ids = set()

                    # Check each result for newly discovered bugs.
                    for result in sequence_results:
                        bug_ids = set(self.bug_detector(result))

                        new_bugs = bug_ids - self.seen_bugs
                        newly_seen.update(new_bugs)
                        self.seen_bugs.update(bug_ids)
                        case_bug_ids.update(bug_ids)

                    results.append({
                        "inputs": case,
                        "bug_ids": sorted(case_bug_ids),
                        "error": None,
                    })

                except Exception as exc:
                    # Record a failure and continue with other cases.
                    results.append({
                        "inputs": case,
                        "bug_ids": [],
                        "error": f"{type(exc).__name__}: {exc}",
                    })

        finally:
            # Stop measurement even if execution unexpectedly fails.
            cov.stop()

        # Calculate statement coverage for the target file.
        analysis = cov.analysis2(target_file)
        statements = set(analysis[1])
        missing_statements = set(analysis[3])

        executed_statements = statements - missing_statements

        total_statement_lines = len(statements)
        executed_statement_lines = sorted(executed_statements)

        coverage_percentage = (
            100.0 * len(executed_statements) / total_statement_lines
            if total_statement_lines
            else 100.0
        )

        # Count target calls attempted by the strategy.
        target_calls = (
            sum(len(case) for case in cases)
            if strategy == 3
            else len(results)
        )

        return {
            "strategy": strategy,
            "tests_executed": len(results),
            "target_calls_executed": target_calls,
            "new_bug_ids": sorted(newly_seen),
            "results": results,
            "execution_time_seconds": (
                time.perf_counter() - started
            ),
            "budget_cost": cost,
            "coverage": round(coverage_percentage, 2),

            # Added for cumulative coverage tracking in the RL environment.
            "executed_statement_lines": executed_statement_lines,
            "total_statement_lines": total_statement_lines,
        }

    def _generate_cases(self, strategy: int) -> list:
        """Generate inputs for the selected testing strategy."""

        if strategy == 0:  # Random testing
            return [
                (
                    self.rng.choice([-100, -1, 0, 1, 10, 100, 1000]),
                    self.rng.choice(["ID1", "ID2", "", None]),
                )
                for _ in range(10)
            ]

        if strategy == 1:  # Boundary-value testing
            return [
                (-1, "ID1"),
                (0, "ID1"),
                (1, "ID1"),
                (99, "ID1"),
                (100, "ID1"),
                (101, "ID1"),
                (100, ""),
                (100, None),
            ]

        if strategy == 2:  # Input mutation
            seeds = [
                (100, "ID1"),
                (10, "ID2"),
            ]

            cases = []

            for amount, identifier in seeds:
                cases.extend([
                    (
                        amount + self.rng.choice([-1, 1]),
                        identifier,
                    ),
                    (amount, ""),
                    (amount, None),
                ])

            return cases

        # Strategy 3: Sequence generation
        return [
            [(100, "ID1"), (0, "ID2")],
            [(10, "ID3"), (-1, "ID4")],
            [(0, "ID5"), (100, "")],
        ]

    def _execute_sequence(
        self, sequence: list[tuple]
    ) -> list:
        """Execute target calls in the given order."""
        return [
            self.target(*inputs)
            for inputs in sequence
        ]
