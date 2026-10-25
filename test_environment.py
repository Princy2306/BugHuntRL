
from environment import BugHuntEnv

env = BugHuntEnv(test_budget=5)

obs, info = env.reset(seed=42)

print("Initial observation:", obs)

for i in range(5):
    action = env.action_space.sample()

    obs, reward, terminated, truncated, info = (
        env.step(action)
    )

    print(f"\nTest {i + 1}")
    print("Action:", action)
    print("Reward:", reward)
    print("Bugs found:", info["bug_ids"])
    print("Observation:", obs)

    if terminated or truncated:
        print("Episode finished!")
        break

env.close()
