
from stable_baselines3 import PPO
from environment import BugHuntEnv

env = BugHuntEnv(test_budget=20)
model = PPO.load("bughunt_ppo")

obs, info = env.reset(seed=42)

print("Testing the trained agent:\n")

for step in range(10):
    action, _ = model.predict(obs, deterministic=True)
    action = int(action)

    names = {
        0: "Normal payment",
        1: "Negative payment",
        2: "Zero payment",
        3: "Missing payment ID"
    }

    obs, reward, terminated, truncated, info = env.step(action)

    print(f"Step: {step + 1}")
    print("Chosen action:", names[action])
    print("Reward:", reward)
    print("New bugs:", info["bug_ids"])
    print()

    if terminated or truncated:
        break

env.close()
