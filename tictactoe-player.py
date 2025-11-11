# File:    tictactoe-player.py
# Topic:   Search
# Course:  CSI480 (Artificial Intelligence)
# Date:    October 9, 2025
# Description: Determine utility of particular starting
#              configuration for X in tic-tac-toe game
#              using minimax.

import random

# Represent game as 1-dimensional list.
# I.e., the following game:
#
#   +---+---+---+
#   |   | X |   |
#   +---+---+---|
#   | O | X |   |
#   +---+---+---+
#   |   |   |   |
#   +---+---+---+
#
# is represented as [0, 1, 0, -1, 1, 0, 0, 0, 0].
#
# An empty slot is symbolized by the number 0,
# player X as 1, player O as -1.

# Constants
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY_SLOT = " "

def print_config(config):
    # Map numbers -1, 0 1 to display player characters instead
    display_config = []
    for mark in config:
        if mark == 1:
            display_config.append(PLAYER_X)
        elif mark == -1:
            display_config.append(PLAYER_O)
        else:
            display_config.append(EMPTY_SLOT)
    print("+---+---+---+")
    print("| {0} | {1} | {2} |".format(*display_config[0:3]))
    print("+---+---+---+")
    print("| {0} | {1} | {2} |".format(*display_config[3:6]))
    print("+---+---+---+")
    print("| {0} | {1} | {2} |".format(*display_config[6:9]))
    print("+---+---+---+")



#def print_config(config):
#    print("+----+----+----+")
#    print("| {0:2d} | {1:2d} | {2:2d} |".format(*config[0:3]))
#    print("+----+----+----+")
#    print ("| {0:2d} | {1:2d} | {2:2d} |".format(*config[3:6]))
#    print("+----+----+----+")
#    print ("| {0:2d} | {1:2d} | {2:2d} |".format(*config[6:9]))
#    print("+----+----+----+")

def successors(config, player):
    succ_configs = []
    
    for pos in range(0, 9):
        if config[pos] == 0:  # empty
            new_config = config[:]  # copy original config
            new_config[pos] = player  # place mark for current player (1 or -1)
            succ_configs.append(new_config)
    
    return succ_configs

def winner(config):
    # Record all possible winning rows, columns, diagonals.
    win_indices = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                   [0, 3, 6], [1, 4, 7], [2, 5, 8],
                   [0, 4, 8], [2, 4, 6]]

    # Sum how many positions marked for each player.
    # If sum comes out +3 or -3, we know it's a win
    # for either X or O respectively.
    for indices in win_indices:
        count = 0
        for i in indices:
            count += config[i]
        if abs(count) == len(indices):  # entire row/col/diagonal?
            return -1 if count < 0 else 1  # return whether player 1 or -1

    return 0  # no winner yet (or a "draw" if all positions filled)

def minimax(config, player, level):
    utility = winner(config)

    if utility == 0:  # not a terminal state
        succ_configs = successors(config, player)

        if succ_configs:  # more places to mark (not a "draw")
            # Generate successors and determine utility
            # for each recursively.
            scores = [minimax(c, -player, level+1) for c in succ_configs]

            if player == 1:  # MAX level
                utility = max(scores)
            elif player == -1:  # MIN level
                utility = min(scores)

    print("Utility:", utility, "who moved:", -player, "level:", level)
    print_config(config)

    return utility

# Current configuration used as starting point.
# Assuming optimal play (each player trying to win), will it be
# a win for player X (1), a win for player O (-1) or a draw (0)?

current_config = [1, 1, 0, -1, -1, 0, -1, 1, 0]
print("Winner:", minimax(config=current_config, player=1, level=0))
