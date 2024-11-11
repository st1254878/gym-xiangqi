import numpy as np
import random
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.constants import ALLY


class TestAgent:
    """
    This is the implementation of the simplest
    agent possible to play the game of Xiang Qi.
    The agent will simply choose a random move
    out of all the possible moves and return that.
    """
    def __init__(self):
        pass

    def move(self, env):
        actions = (env.ally_actions if env.turn == ALLY else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]
        best_reward = -float('inf')
        best_moves = []

        # Loop through all legal moves and simulate each one
        for move in legal_moves:
            # Temporarily perform the move to get the reward
            pieces, s,e = action_space_to_move(move)
            #print(pieces,s,e)
            if s==e:
                reward = 0
            elif env.state[e[0]][e[1]] != 0:
                reward = 1
            else: reward = 0
            # Update the list of best moves
            if reward > best_reward:
                best_reward = reward
                best_moves = [move]
            elif reward == best_reward:
                best_moves.append(move)

        # Randomly select one of the moves with the highest reward
        return random.choice(best_moves) if best_moves else legal_moves[0]
