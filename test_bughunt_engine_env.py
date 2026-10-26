
import numpy as np


from testing_engine import TestingEngine
from bughunt_engine_env import BugHuntEngineEnv


def test_reset_returns_valid_observation():
    env = BugHuntEngineEnv(seed=42)
    observation, info = env.reset()

    assert env.observation_space.contains(observation)
    assert info == {}


def test_step_executes_real_testing_engine():
    env = BugHuntEngineEnv(seed=42)
    env.reset(seed=42)

    observation, reward, terminated, truncated, info = env.step(1)

    assert env.observation_space.contains(observation)
    assert isinstance(reward, float)
    assert info["action"] == 1
    assert info["strategy_cost"] == 8
    assert info["tests_executed_this_step"] > 0
    assert info["measured_coverage_percent"] >= 0
    assert env.remaining_budget == 92


def test_budget_is_respected():
    env = BugHuntEngineEnv(seed=42)
    env.reset(seed=42)

    env.remaining_budget = 5
    observation, reward, terminated, truncated, info = env.step(1)

    assert terminated is True
    assert info["reason"] == "insufficient_budget"
    assert env.remaining_budget == 5




def test_cumulative_coverage_never_decreases():
    env = BugHuntEngineEnv(seed=42)
    env.reset(seed=42)

    previous_coverage = 0.0

    for action in [1, 0, 2, 3]:
        if TestingEngine.STRATEGY_COSTS[action] > env.remaining_budget:
            break

        observation, reward, terminated, truncated, info = env.step(action)

        current_coverage = info["cumulative_coverage_fraction"]

        assert current_coverage >= previous_coverage
        assert 0.0 <= current_coverage <= 1.0

        previous_coverage = current_coverage

        if terminated or truncated:
            break
