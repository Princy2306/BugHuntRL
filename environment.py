
import gymnasium as gym
from gymnasium import spaces
import numpy as np

from payment_system import process_payment


class BugHuntEnv(gym.Env):

    def __init__(self, test_budget=20):
        super().__init__()

        self.test_budget = test_budget

        # Four possible testing strategies
        self.action_space = spaces.Discrete(4)

        # State: 4 visited flags, bug count, remaining budget
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(6,),
            dtype=np.float32
        )

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.visited = np.zeros(4, dtype=np.float32)
        self.unique_bugs = set()
        self.remaining = self.test_budget

        return self._get_obs(), {}

    def _get_obs(self):
        return np.concatenate([
            self.visited,
            np.array([
                min(len(self.unique_bugs) / 10, 1.0),
                self.remaining / self.test_budget
            ], dtype=np.float32)
        ]).astype(np.float32)

    def step(self, action):
        # Action 0: normal payment
        # Action 1: negative payment
        # Action 2: zero payment
        # Action 3: missing payment ID
        tests = [
            (100, "PAY001"),
            (-10, "PAY002"),
            (0, "PAY003"),
            (100, "")
        ]

        amount, payment_id = tests[int(action)]

        result = process_payment(amount, payment_id)
        reward = 0.0

        # Reward exploration of a new test category
        if self.visited[action] == 0:
            self.visited[action] = 1
            reward += 1.0

        # Reward discovery of a unique bug
        new_bugs = set(result["bug_ids"]) - self.unique_bugs

        if new_bugs:
            reward += 10.0 * len(new_bugs)
            self.unique_bugs.update(new_bugs)

        self.remaining -= 1

        terminated = False
        truncated = self.remaining <= 0

        info = {
            "bug_ids": list(new_bugs)
        }

        return (
            self._get_obs(),
            reward,
            terminated,
            truncated,
            info
        )
