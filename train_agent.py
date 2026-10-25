
from stable_baselines3 import PPO
from bughunt_env import BugHuntEnv


def main():
    env = BugHuntEnv()

    model = PPO(
        "MlpPolicy",
        env,
        n_steps=32,
        batch_size=16,
        seed=42,
        verbose=1,
    )

    model.learn(total_timesteps=100)
    model.save("bughunt_ppo_initial")

    print("Initial PPO checkpoint saved.")


if __name__ == "__main__":
    main()
