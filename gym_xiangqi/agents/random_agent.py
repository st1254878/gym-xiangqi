import numpy as np
import random

from gym_xiangqi.constants import ALLY


class RandomAgent:
    """
    This is the implementation of the simplest
    agent possible to play the game of Xiang Qi.
    The agent will simply choose a random move
    out of all the possible moves and return that.
    """
    def __init__(self):
        pass

    def move(self, env):
        """
        Make a random move based on the environment.
        """
        actions = (env.ally_actions if env.turn == ALLY
                   else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]
        ind = random.randint(0, len(legal_moves)-1)
        return legal_moves[ind]

    def check_move_operation(self, action):
        piece_id, r = divmod(action, pow(32, 2))
        start_val, end_val = divmod(r, 32)
        start = [0, 0]
        end = [0, 0]
        start[0], start[1] = divmod(start_val, 8)
        end[0], end[1] = divmod(end_val, 8)
        return piece_id + 1, start, end