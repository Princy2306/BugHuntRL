from bughunt_env import BugHuntEnv

for seed in range(5):
    env = BugHuntEnv()
    obs, _ = env.reset(seed=seed)

    total_reward = 0
    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

        if terminated or truncated:
            break

    print(
        f"Seed {seed}: reward={total_reward:.2f}, "
        f"bugs={obs[2]:.0f}, coverage={obs[1]:.2f}, "
        f"tests={obs[3]:.0f}"
    )