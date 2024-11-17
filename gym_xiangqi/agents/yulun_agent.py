import numpy as np
import random
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.constants import ALLY, ALIVE, ORTHOGONAL, BOARD_COLS, BOARD_ROWS, EMPTY, COVER_BOARD




class YulunAgent:


    def __init__(self):
        pass

    def move(self, env):
        actions = (env.ally_actions if env.turn == ALLY else env.enemy_actions)
        cannon1 = (env.ally_piece[10] if env.turn == ALLY else env.enemy_piece[10])
        cannon2 = (env.ally_piece[11] if env.turn == ALLY else env.enemy_piece[11])
        legal_moves = np.where(actions == 1)[0]
        eat_moves = []
        flip_moves = []
        cannon_flip = []
        last_considered = []
        # Loop through all legal moves and simulate each one
        for move in legal_moves:
            # Temporarily perform the move to get the reward
            pieces, s, e = action_space_to_move(move)

            # print(pieces,s,e)
            if s == e:
                if cannon1.state == ALIVE or cannon2.state == ALIVE:
                    if (env.turn == ALLY and (env.ally_piece[pieces].row == s[0] and env.ally_piece[pieces].col == s[1])):
                        if self.check_cannon_pos(s, env):
                            cannon_flip.append(move)
                        else:
                            flip_moves.append(move)
                    else:
                        flip_moves.append(move)
                else:
                    flip_moves.append(move)
            elif env.state[e[0]][e[1]] != 0:
                if not(self.check_exange(s,e,env)):
                    eat_moves.append(move)
                else:
                    last_considered.append(move)
            else:
                last_considered.append(move)
        # Randomly select one of the moves with the highest reward
        if eat_moves != []:
            return random.choice(eat_moves)
        elif cannon_flip != []:
            return random.choice(cannon_flip)
        elif flip_moves != []:
            return random.choice(flip_moves)
        elif last_considered != []:
            return random.choice(last_considered)
        else:
            return []

        #return random.choice(best_moves) if best_moves else legal_moves[0]

    def check_cannon_pos(self, s, env):
        for dir in ORTHOGONAL:
            nxtr = s[0]
            nxtc = s[1]
            has_pieces_between = False
            while True:
                nxtr += dir[0]
                nxtc += dir[1]
                if nxtr >= BOARD_ROWS or nxtr < 0 or nxtc >=BOARD_COLS or nxtc < 0:
                    break
                if env._cover_state[nxtr][nxtc] == 0 and env.state[nxtr][nxtc]*env.state[s[0]][s[1]] < 0:
                    if has_pieces_between:
                        return True
                if not(has_pieces_between):
                    if env.state[nxtr][nxtc] != 0:
                        has_pieces_between = True
                elif env.state[nxtr][nxtc] != 0:
                    break
        return False

    def check_exange(self, s, e, env):
        my_piece = abs(env.state[s[0]][s[1]])
        for dir in ORTHOGONAL:
            nxtr = e[0]
            nxtc = e[1]
            nxtr += dir[0]
            nxtc += dir[1]
            if nxtr >= BOARD_ROWS or nxtr < 0 or nxtc >=BOARD_COLS or nxtc < 0:
                continue
            if env._cover_state[nxtr][nxtc] == 0 and env.state[nxtr][nxtc] * env.state[s[0]][s[1]] < 0:
                if my_piece == 1:
                    compare_id = 0
                else:
                    compare_id = my_piece // 2
                if abs(env.state[nxtr][nxtc]) == 1:
                    target_id = 0
                else:
                    target_id = abs(env.state[nxtr][nxtc]) // 2

                if compare_id >= target_id or (compare_id == 0 and target_id >= 6):
                    return True

        return False
