
from stable_baselines3 import PPO
from environment import BugHuntEnv

# Create the environment
env = BugHuntEnv(test_budget=20)

# Create the PPO agent
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    seed=42,
    n_steps=128,
    batch_size=64
)

# Train the agent
model.learn(total_timesteps=10_000)

# Save the trained model
model.save("bughunt_ppo")

print("Training completed successfully!")

env.close()
