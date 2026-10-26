
from stable_baselines3 import PPO
from bughunt_env import BugHuntEnv

model = PPO.load("bughunt_ppo_updated")

for seed in range(5):
    env = BugHuntEnv()
    obs, _ = env.reset(seed=seed)

    total_reward = 0.0

    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

        if terminated or truncated:
            break

    print(
        f"Seed {seed}: reward={total_reward:.2f}, "
        f"bugs={obs[2]:.0f}, coverage={obs[1]:.2f}, "
        f"tests={obs[3]:.0f}"
    )

    env.close()
