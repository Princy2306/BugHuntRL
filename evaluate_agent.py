
from stable_baselines3 import PPO
from environment import BugHuntEnv


def evaluate_agent(model=None, episodes=100):
    total_bugs = 0
    successful_episodes = 0
    discovery_steps = []

    for episode in range(episodes):
        env = BugHuntEnv(test_budget=20)
        obs, info = env.reset(seed=episode)

        for step in range(20):
            if model is None:
                # Random baseline
                action = env.action_space.sample()
            else:
                # Trained PPO agent
                action, _ = model.predict(
                    obs, deterministic=True
                )
                action = int(action)

            obs, reward, terminated, truncated, info = (
                env.step(action)
            )

            if info["bug_ids"]:
                discovery_steps.append(step + 1)

            if terminated or truncated:
                break

        bugs_found = len(env.unique_bugs)
        total_bugs += bugs_found

        if bugs_found > 0:
            successful_episodes += 1

        env.close()

    print("Episodes:", episodes)
    print(
        "Episodes finding at least one bug:",
        successful_episodes
    )
    print(
        "Bug discovery rate:",
        f"{successful_episodes / episodes * 100:.1f}%"
    )
    print(
        "Average unique bugs per episode:",
        f"{total_bugs / episodes:.2f}"
    )

    if discovery_steps:
        print(
            "Average tests until bug discovery:",
            f"{sum(discovery_steps) / len(discovery_steps):.2f}"
        )
    else:
        print("No bugs discovered.")


if __name__ == "__main__":
    model = PPO.load("bughunt_ppo")

    print("\n--- Trained PPO Agent ---")
    evaluate_agent(model)

    print("\n--- Random Baseline ---")
    evaluate_agent(model=None)
