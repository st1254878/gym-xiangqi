from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.agents import TestAgent
from gym_xiangqi.constants import ALLY, PIECE_ID_TO_NAME
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.envs import XiangQiEnv
import gym
import time
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME, ALLY
)

def main():
    env = XiangQiEnv(RED)
    env.render()
    agent = RandomAgent()
    # env.reset()
    done = False
    round = 0
    while not done:
        # Add a slight delay to properly visualize the game.

        if round % 2==0:
            agent = TestAgent()
            print("can eat i eat!")
            action = agent.move(env)
        else:
            agent = RandomAgent()
            print("do anything!")
            action = agent.move(env)
        time.sleep(2)
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
    env.close()


if __name__ == '__main__':
    main()
