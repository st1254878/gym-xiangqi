import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# 训练部分
env = make_vec_env("CartPole-v1", n_envs=4)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("ppo_cartpole")
del model  # 清除模型，测试读取功能

# 评估部分
model = PPO.load("ppo_cartpole")

# 使用单一环境进行渲染评估
env = gym.make("CartPole-v1", render_mode="human")  # 设置渲染模式为 human
obs, info = env.reset()  # 解包 obs 和 info

for _ in range(1000):  # 限制步数
    action, _states = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)  # 现在返回 5 个值
    if terminated or truncated:  # 判断是否结束
        obs, info = env.reset()  # 再次解包

env.close()
