
import gymnasium as gym
from gymnasium import spaces
import numpy as np


class BugHuntEnv(gym.Env):
    """RL environment for learning efficient software testing."""

    def __init__(self):
        super().__init__()

        # Four testing strategies: actions 0, 1, 2, 3
        self.action_space = spaces.Discrete(4)

        # [remaining_budget, coverage, bugs_found,
        #  tests_executed, recent_success_rate]
        self.observation_space = spaces.Box(
            low=np.array([0, 0.0, 0, 0, 0.0], dtype=np.float32),
            high=np.array([100, 1.0, 20, 100, 1.0], dtype=np.float32),
            dtype=np.float32
        )
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.remaining_budget = 100
        self.coverage_fraction = 0.0
        self.unique_bugs_found = 0
        self.tests_executed = 0

        # Store the outcomes of the five most recent tests.
        self.recent_outcomes = []
        self.discovered_bugs = set()
        self.covered_units = set()
        self.recent_outcomes = []

        observation = np.array([
            self.remaining_budget,
            self.coverage_fraction,
            self.unique_bugs_found,
            self.tests_executed,
            0.0  # No testing history yet
        ], dtype=np.float32)

        info = {}

        return observation, info
    
    def step(self, action):
        costs = {0: 5, 1: 8, 2: 6, 3: 10}
        cost = costs[int(action)]

        if cost > self.remaining_budget:
            raise ValueError("Insufficient budget for this action.")

        # Simulate strategy-specific testing outcomes.
        # Each strategy has a different set of opportunities.
        opportunities = {
            0: {"bugs": [0, 1, 2, 3, 4],
                "coverage": [0, 1, 2, 3, 4]},
            1: {"bugs": [5, 6, 7, 8, 9],
                "coverage": [5, 6, 7, 8, 9]},
            2: {"bugs": [10, 11, 12, 13, 14],
                "coverage": [10, 11, 12, 13, 14]},
            3: {"bugs": [15, 16, 17, 18, 19],
                "coverage": [15, 16, 17, 18, 19]},
        }

        candidates = opportunities[int(action)]

        # Use the environment's seeded random generator.
        bug_candidates = [
            bug for bug in candidates["bugs"]
            if bug not in self.discovered_bugs
        ]
        coverage_candidates = [
            unit for unit in candidates["coverage"]
            if unit not in self.covered_units
        ]

        new_bugs = []
        new_coverage = []

        if bug_candidates and self.np_random.random() < 0.5:
            bug = int(self.np_random.choice(bug_candidates))
            self.discovered_bugs.add(bug)
            new_bugs.append(bug)

        if coverage_candidates and self.np_random.random() < 0.7:
            unit = int(self.np_random.choice(coverage_candidates))
            self.covered_units.add(unit)
            new_coverage.append(unit)

        self.remaining_budget -= cost
        self.tests_executed += 1

        bug_count = len(new_bugs)
        coverage_gain = len(new_coverage) / 20

        # Redundant means neither bugs nor coverage were discovered.
        redundant = int(bug_count == 0 and coverage_gain == 0)

        reward = (
            10 * bug_count
            + 5 * coverage_gain
            - 2 * redundant
            - 0.1 * cost
        )

        self.recent_outcomes.append(
            int(bug_count > 0 or coverage_gain > 0)
        )
        self.recent_outcomes = self.recent_outcomes[-5:]

        self.coverage_fraction = len(self.covered_units) / 20
        self.unique_bugs_found = len(self.discovered_bugs)

        recent_success_rate = (
            sum(self.recent_outcomes) / len(self.recent_outcomes)
            if self.recent_outcomes else 0.0
        )

        observation = np.array([
            self.remaining_budget,
            self.coverage_fraction,
            self.unique_bugs_found,
            self.tests_executed,
            recent_success_rate
        ], dtype=np.float32)

        terminated = self.remaining_budget < 5
        truncated = False

        info = {
            "action": int(action),
            "strategy_cost": cost,
            "new_bugs": new_bugs,
            "new_coverage_units": new_coverage,
            "coverage_gain": coverage_gain,
            "redundant": bool(redundant)
        }

        return observation, float(reward), terminated, truncated, info

