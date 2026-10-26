
import csv

from stable_baselines3 import PPO
from src.bughunt_engine_env import BugHuntEngineEnv


MODEL_PATH = "models/bughunt_engine_ppo"
NUM_EPISODES = 20
INITIAL_BUDGET = 100
RESULTS_FILE = "results/ppo_evaluation_results.csv"


def main():
    env = BugHuntEngineEnv(seed=42)
    model = PPO.load(MODEL_PATH, env=env)

    rows = []
    rewards = []
    bug_counts = []
    coverage_percentages = []
    budgets_used = []
    strategy_counts = {i: 0 for i in range(4)}

    strategy_names = {
        0: "Random Testing",
        1: "Boundary-Value Testing",
        2: "Input Mutation",
        3: "Sequence Generation",
    }

    for episode in range(NUM_EPISODES):
        observation, _ = env.reset(seed=42 + episode)

        total_reward = 0.0
        terminated = False
        truncated = False

        while not (terminated or truncated):
            action, _ = model.predict(
                observation,
                deterministic=True,
            )

            action = int(action)
            strategy_counts[action] += 1

            observation, reward, terminated, truncated, info = (
                env.step(action)
            )

            total_reward += reward

        bugs_found = env.unique_bugs_found
        coverage = env.coverage_fraction * 100
        budget_used = INITIAL_BUDGET - env.remaining_budget

        rewards.append(total_reward)
        bug_counts.append(bugs_found)
        coverage_percentages.append(coverage)
        budgets_used.append(budget_used)

        rows.append({
            "episode": episode + 1,
            "total_reward": round(total_reward, 2),
            "unique_bugs_found": bugs_found,
            "coverage_percent": round(coverage, 2),
            "initial_budget": INITIAL_BUDGET,
            "budget_used": budget_used,
            "budget_remaining": env.remaining_budget,
        })

        print(
            f"Episode {episode + 1}: "
            f"Reward={total_reward:.2f}, "
            f"Bugs={bugs_found}, "
            f"Coverage={coverage:.2f}%, "
            f"Budget used={budget_used}, "
            f"Budget remaining={env.remaining_budget}"
        )

    with open(
        RESULTS_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )
        writer.writeheader()
        writer.writerows(rows)

    print("\n--- PPO Evaluation Summary ---")
    print(f"Episodes: {NUM_EPISODES}")
    print(f"Average reward: {sum(rewards) / NUM_EPISODES:.2f}")
    print(
        f"Average unique bugs: "
        f"{sum(bug_counts) / NUM_EPISODES:.2f}"
    )
    print(
        f"Average cumulative coverage: "
        f"{sum(coverage_percentages) / NUM_EPISODES:.2f}%"
    )
    print(
        f"Average budget used: "
        f"{sum(budgets_used) / NUM_EPISODES:.2f}"
    )
    print(
        f"Average budget remaining: "
        f"{INITIAL_BUDGET - sum(budgets_used) / NUM_EPISODES:.2f}"
    )

    print("\nStrategy selection counts:")
    for action, name in strategy_names.items():
        print(f"{name}: {strategy_counts[action]}")

    print(f"\nPer-episode results saved to {RESULTS_FILE}")

    env.close()


if __name__ == "__main__":
    main()
