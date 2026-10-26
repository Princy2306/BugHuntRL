
from stable_baselines3 import PPO
from bughunt_engine_env import BugHuntEngineEnv


def main():
    # Use the environment connected to the actual TestingEngine
    env = BugHuntEngineEnv(seed=42)

    model = PPO(
        "MlpPolicy",
        env,
        n_steps=32,
        batch_size=16,
        seed=42,
        verbose=1,
    )

    model.learn(total_timesteps=5000)

    # Save to a new checkpoint to protect the existing model
    model.save("bughunt_engine_ppo")

    print("Engine-integrated PPO checkpoint saved.")

    env.close()


if __name__ == "__main__":
    main()

