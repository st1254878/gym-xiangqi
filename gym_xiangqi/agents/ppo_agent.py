import gym
from gym_xiangqi.envs import XiangQiEnv
from stable_baselines3 import PPO
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME, ALLY
)
# Create the environment
env = XiangQiEnv(RED)

# Create the PPO agent
model = PPO('MlpPolicy', env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)
model.save("ppo_dark_chess")
del model # remove to demonstrate saving and loading
# Test the trained agent
model = PPO.load("ppo_cartpole")
obs = env.reset()

while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
