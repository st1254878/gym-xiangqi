
from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.agents import TestAgent
from gym_xiangqi.agents import YulunAgent
from gym_xiangqi.agents import select_color
from gym_xiangqi.constants import ALLY, PIECE_ID_TO_NAME
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.envs import XiangQiEnv
import gym
import time
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME, ALLY
)

import time
import matplotlib.pyplot as plt
from collections import Counter





def main():
    results = []  # 用来记录每场比赛的结果
    num_games = 100  # 每组对战的局数
    matchups = [
        ("YulunAgent", YulunAgent,"RandomAgent" , RandomAgent),
        ("TestAgent", TestAgent, "YulunAgent", YulunAgent),
        ("TestAgent", TestAgent, "RandomAgent", RandomAgent),
    ]
    for agent1_name, Agent1, agent2_name, Agent2 in matchups:
        print(f"Starting matches: {agent1_name} vs {agent2_name}")
        for game in range(num_games):
            print(f"Game {game + 1} starts!")

            #print(COLOR)

            env = XiangQiEnv(RED)

            env.render()

            # 实例化两个代理
            agent1 = Agent1()
            agent2 = Agent2()
            done = False
            round = 0
            winning = 0
            first_action = RandomAgent()
            action = first_action.move(env)
            env.select_side(action)
            while not done:

                message = "紅棋" if env.turn == ALLY else "黑棋"
                if (round % 2):

                    print(f"Agent2 policy ({agent2_name})控制{message}")

                    action = agent2.move(env)
                    if not action:  # 假设表示 Agent2 没有合法动作
                        winning = 1  # Agent1 胜利
                else:
                    print(f"Agent1 policy ({agent1_name})控制{message}")
                    if round!= 0:
                        action = agent1.move(env)
                        if not action:  # 假设表示 Agent1 没有合法动作
                            winning = 2  # Agent2 胜利

                if winning != 0:
                    break
                else:
                    _, reward, done, _ = env.step(action)
                    turn = "Ally" if env.turn == ALLY else "Enemy"
                    move = action_space_to_move(action)
                    piece = PIECE_ID_TO_NAME[move[0]]

                    print(f"Round: {round}")
                    print(f"{turn} made the move {piece} from {move[1]} to {move[2]}.")
                    print(f"Reward: {reward}")
                    print("================")

                    round += 1
                    if round > 1500:
                        # 达到回合限制后，根据棋子数决定胜负
                        redmax, blackmax = calculate_remaining_pieces(env)
                        if redmax < blackmax or (redmax == 0 and blackmax >= 6):
                            winning = 1
                        elif redmax > blackmax or (blackmax == 0 and redmax >= 6):
                            winning = 2
                        else:
                            winning = 3
                        break
                    time.sleep(0.01)  # 减慢游戏节奏以便观察
                env.render()

            # 关闭环境并记录结果
            env.close()
            if winning == 1:
                results.append((agent1_name, agent2_name, f"{agent1_name} wins"))
            elif winning == 2:
                results.append((agent1_name, agent2_name, f"{agent2_name} wins"))
            else:
                results.append((agent1_name, agent2_name, "Draw"))

            print(f"Game {game + 1} ends! Winner: {results[-1]}")

    # 绘制统计结果
    plot_results(results)


def calculate_remaining_pieces(env):
    redmax = 0
    blackmax = 0
    for i in range(1, 17):
        if env.ally_piece[i].is_alive():
            if i == 1:
                redmax = 0
            else:
                redmax = i // 2
    for i in range(1, 17):
        if env.enemy_piece[i].is_alive():
            if i == 1:
                blackmax = 0
            else:
                blackmax = i // 2
    return redmax, blackmax


def plot_results(results):
    matchup_results = {}
    for agent1_name, agent2_name, result in results:
        matchup = f"{agent1_name} vs {agent2_name}"
        if matchup not in matchup_results:
            matchup_results[matchup] = {"Draw": 0, f"{agent1_name} wins": 0, f"{agent2_name} wins": 0}
        matchup_results[matchup][result] += 1

    for matchup, counts in matchup_results.items():
        labels = list(counts.keys())
        values = list(counts.values())

        plt.figure(figsize=(8, 4))
        plt.bar(labels, values, color=['red', 'blue', 'green'])
        plt.xlabel("Result")
        plt.ylabel("Number of Games")
        plt.title(f"Results for {matchup}")
        plt.xticks(rotation=15)
        plt.show()
if __name__ == "__main__":
    main()