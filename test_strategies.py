from bughunt_env import BugHuntEnv

env = BugHuntEnv()
obs, _ = env.reset(seed=42)

for action in range(4):
    obs, reward, terminated, truncated, info = env.step(action)
    print(
        f"Action {action}: reward={reward:.2f}, "
        f"new_bugs={info['new_bugs']}, "
        f"new_coverage={info['new_coverage_units']}, "
        f"budget={obs[0]}"
    )