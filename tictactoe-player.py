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

#---Constants----#
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY_SLOT = " "

#can be used for negative and positive 
#infinity since they are outside
#utility range of -1 0 1
ALPHA_INIT = -2
BETA_INIT = 2

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

def minimax(config, player, level, alpha, beta):
    utility = winner(config)

    if utility == 0:  # not a terminal state
        succ_configs = successors(config, player)

        if succ_configs:  # more places to mark (not a "draw")
            #scores = [minimax(c, -player, level+1) for c in succ_configs]

            if player == 1:  # MAX level
                best_utility = ALPHA_INIT # negative "infinity"
                for c in succ_configs:
                    # Generate successors and determine utility
                    # for each recursively.
                    val = minimax(c, -player, level+1, alpha, beta)
                    best_utility = max(best_utility, val)
                    alpha = max(alpha, best_utility)
                    if beta <= alpha:
                        break #beta cut off
                utility = best_utility

            elif player == -1:#MIN level
                best_utility = BETA_INIT # Positive "infinity"
                for c in succ_configs:
                    # Generate successors and determine utility
                    # for each recursively.
                    val = minimax(c, -player, level+1, alpha, beta)
                    best_utility = min(best_utility, val)
                    beta = min(beta, best_utility)
                    if beta <= alpha:
                        break # Alpha cut off
                utility = best_utility
            
        # If there were no succ_configs (is a draw) utility remains 0 as set by winner()

    #print("Utility:", utility, "who moved:", -player, "level:", level)
    #print_config(config)

    return utility

def computer_best_move(config, player):
    succ_configs = successors(config, player)
    best_move = None
    # "infinity" values
    alpha = ALPHA_INIT
    beta = BETA_INIT

    if player == 1:  # MAX player
        best_util = ALPHA_INIT
        for move in succ_configs:
            # -player is opponent, call minimax from new board state for them starting
            # at level one
            val = minimax(move, -player, 1, alpha, beta)
            if val > best_util:
                best_util = val
                best_move = move
            alpha = max(alpha, best_util)
            #prune at root level
            if beta <= alpha:
                break
    else:  # MIN player
        best_util = BETA_INIT
        for move in succ_configs:
            val = minimax(move, -player, 1, alpha, beta)
            if val < best_util:
                best_util = val
                best_move = move
            beta = min(beta, best_util)
            if beta <= alpha:
                break
    return best_move

def get_user_move(config):
    while True:
        try:
            move_str = input(f"Your turn ({PLAYER_X}). Enter position (0-8): ")
            move = int(move_str)
            
            if move < 0 or move > 8:
                print("Invalid move.")
            elif config[move] != 0:
                print("Position is already taken.")
            else:
                # apply valid move
                new_config = config[:]
                new_config[move] = 1  # User is always player 1
                return new_config
        
        except ValueError:
            print("Invalid input.")

def main_game_loop():
    current_config = [0, 0, 0, 0, 0, 0, 0, 0, 0] # Blank board
    current_player = 1  # User starts first
    
    print("You are 'X'. Enter a number 0-8 to make your move.")
    print("The board positions are:")
    print("+---+---+---+")
    print("| 0 | 1 | 2 |")
    print("+---+---+---+")
    print("| 3 | 4 | 5 |")
    print("+---+---+---+")
    print("| 6 | 7 | 8 |")
    print("+---+---+---+")
    
    while True:
        if current_player == 1:
            # User turn
            current_config = get_user_move(current_config)
            print_config(current_config)
        else:
            # CPU turn
            print("CPU's turn...")
            old_config = current_config[:] #store old board
            current_config = computer_best_move(current_config, current_player)

            # Figure out what move the computer made to print it
            move_made = -1
            if current_config: # did it return a move?
                for i in range(9):
                    if old_config[i] != current_config[i]:
                        move_made = i
                        break
                print(f"CPU chose position {move_made}")
                print_config(current_config)


        # Check for game over
        game_winner = winner(current_config)
        if game_winner != 0:
            if game_winner == 1:
                print("Game over! X wins!")
            else:
                print("Game over! O wins!")
            break

        #Draw if no winner and no more valid moves
        if game_winner == 0 and not successors(current_config, -current_player):
            print("Game over. It's a draw.")
            break
        
        # Switch players between X to O or O to X
        current_player = -current_player


# Start game
if __name__ == "__main__":
    main_game_loop()