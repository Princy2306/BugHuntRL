
import gymnasium as gym
import numpy as np

from src.sample_app import sample_target
from src.testing_engine import TestingEngine


class BugHuntEngineEnv(gym.Env):
    """Gymnasium environment backed by the actual TestingEngine."""

    metadata = {"render_modes": []}

    def __init__(self, seed=42):
        super().__init__()

        self.action_space = gym.spaces.Discrete(4)

        # [remaining_budget, coverage_fraction, bugs_found,
        #  tests_executed, recent_success_rate]
        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0.0, 0, 0, 0.0], dtype=np.float32),
            high=np.array([100, 1.0, 20, 200, 1.0], dtype=np.float32),
            dtype=np.float32,
        )

        self.seed_value = seed
        self.engine = None

        self.remaining_budget = 100
        self.coverage_fraction = 0.0
        self.unique_bugs_found = 0
        self.tests_executed = 0
        self.recent_outcomes = []
        self.discovered_bugs = set()

        # Track cumulative statement coverage across this episode.
        self.covered_statement_lines = set()
        self.total_statement_lines = 0

    def _observation(self):
        recent_success_rate = (
            sum(self.recent_outcomes) / len(self.recent_outcomes)
            if self.recent_outcomes
            else 0.0
        )

        return np.array(
            [
                self.remaining_budget,
                self.coverage_fraction,
                self.unique_bugs_found,
                self.tests_executed,
                recent_success_rate,
            ],
            dtype=np.float32,
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        actual_seed = self.seed_value if seed is None else seed

        self.engine = TestingEngine(
            target=sample_target,
            seed=actual_seed,
        )

        self.remaining_budget = 100
        self.coverage_fraction = 0.0
        self.unique_bugs_found = 0
        self.tests_executed = 0
        self.recent_outcomes = []
        self.discovered_bugs = set()

        # Each episode starts with no covered statements.
        self.covered_statement_lines = set()
        self.total_statement_lines = 0

        return self._observation(), {}

    def step(self, action):
        action = int(action)

        if not self.action_space.contains(action):
            raise ValueError(f"Invalid action: {action}")

        cost = TestingEngine.STRATEGY_COSTS[action]

        if cost > self.remaining_budget:
            return (
                self._observation(),
                0.0,
                True,
                False,
                {
                    "reason": "insufficient_budget",
                    "action": action,
                },
            )

        # Execute the selected strategy using the real testing engine.
        report = self.engine.run(
            strategy=action,
            budget=self.remaining_budget,
        )

        # Update unique bug discoveries.
        new_bugs = set(report["new_bug_ids"])
        self.discovered_bugs.update(new_bugs)

        # Calculate newly covered statements.
        previous_covered_count = len(self.covered_statement_lines)

        self.covered_statement_lines.update(
            report["executed_statement_lines"]
        )

        self.total_statement_lines = report["total_statement_lines"]

        newly_covered_count = (
            len(self.covered_statement_lines) - previous_covered_count
        )

        # Coverage gain is the fraction of all statements newly covered.
        coverage_gain = (
            newly_covered_count / self.total_statement_lines
            if self.total_statement_lines > 0
            else 0.0
        )

        # Redundant means no new bug and no newly covered statement.
        redundant = int(
            not new_bugs and newly_covered_count == 0
        )

        # Preserve the original reward formula.
        reward = (
            10 * len(new_bugs)
            + 5 * coverage_gain
            - 2 * redundant
            - 0.1 * cost
        )

        # Update the environment state.
        self.remaining_budget -= cost
        self.tests_executed += report["tests_executed"]
        self.unique_bugs_found = len(self.discovered_bugs)

        self.coverage_fraction = (
            len(self.covered_statement_lines) / self.total_statement_lines
            if self.total_statement_lines > 0
            else 0.0
        )

        self.recent_outcomes.append(
            int(bool(new_bugs) or newly_covered_count > 0)
        )
        self.recent_outcomes = self.recent_outcomes[-5:]

        # End when no available strategy can be afforded.
        terminated = (
            self.remaining_budget
            < min(TestingEngine.STRATEGY_COSTS.values())
        )

        truncated = False

        info = {
            "action": action,
            "strategy_cost": cost,
            "new_bugs": sorted(new_bugs),
            "measured_coverage_percent": report["coverage"],
            "cumulative_coverage_fraction": self.coverage_fraction,
            "newly_covered_statements": newly_covered_count,
            "total_statement_lines": self.total_statement_lines,
            "coverage_gain": coverage_gain,
            "tests_executed_this_step": report["tests_executed"],
            "target_calls_executed": report["target_calls_executed"],
            "execution_time_seconds": report["execution_time_seconds"],
            "redundant": bool(redundant),
        }

        return (
            self._observation(),
            float(reward),
            terminated,
            truncated,
            info,
        )
