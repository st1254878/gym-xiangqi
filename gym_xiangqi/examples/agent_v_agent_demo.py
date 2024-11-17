from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.agents import TestAgent
from gym_xiangqi.agents import YulunAgent
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
    results = []  # 用來記錄每場比賽的結果
    num_games = 5  # 設定對局次數

    for game in range(num_games):
        print(f"Game {game + 1} starts!")
        env = XiangQiEnv(RED)
        env.render()
        agent1 = YulunAgent()  # 玩家1 (紅方)
        agent2 = TestAgent()  # 玩家2 (黑方)

        done = False
        round = 0
        winning = 0

        while not done:
            if round % 2 == 0:
                print("Agent2 policy (TestAgent)")
                action = agent2.move(env)
                if action == []:  # 假設這表示 Agent2 沒有合法動作
                    winning = 1  # Agent1 獲勝
            else:
                print("Agent1 policy (YulunAgent)")
                action = agent1.move(env)
                if action == []:  # 假設這表示 Agent1 沒有合法動作
                    winning = 2  # Agent2 獲勝

            time.sleep(0.01)  # 減慢遊戲節奏以便觀察

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
                env.render()

        # 關閉環境並記錄結果
        env.close()
        if winning == 1:
            results.append("Agent1 (Yulun)")
        elif winning == 2:
            results.append("Agent2 (Test)")
        else:
            results.append("Draw")  # 假設平局情況需要單獨處理

        print(f"Game {game + 1} ends! Winner: {results[-1]}")

    # 畫出統計結果
    plot_results(results)


def plot_results(results):
    counter = Counter(results)
    labels = list(counter.keys())
    counts = list(counter.values())

    plt.bar(labels, counts, color=['red', 'blue', 'green'])
    plt.xlabel("Result")
    plt.ylabel("Number of Games")
    plt.title("Agent vs Agent Results")
    plt.show()


if __name__ == "__main__":
    main()