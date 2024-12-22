"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # raise NotImplementedError
    # all_items = [item for row in board for item in row]
    cnt_of_x, cnt_of_o = 0, 0
    for row in board:
        for item in row:
            if item == X:
                cnt_of_x += 1
            elif item == O:
                cnt_of_o += 1

    if cnt_of_x == cnt_of_o:
        return X
    elif cnt_of_x > cnt_of_o:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # raise NotImplementedError
    possible_actions = set()
    for row_idx in range(len(board)):
        for field_idx in range(len(board[row_idx])):
            if board[row_idx][field_idx] == EMPTY:
                possible_actions.add((row_idx, field_idx))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # raise NotImplementedError
    row_idx, field_idx = action

    if board[row_idx][field_idx] != EMPTY:
        raise ValueError

    c_board = deepcopy(board)
    cur_player = player(c_board)
    c_board[row_idx][field_idx] = cur_player
    return c_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # raise NotImplementedError
    diagonal_1, diagonal_2 = set(), set()
    l_board = len(board)
    vertical_list = list(zip(*board))
    for row_idx in range(l_board):
        # Check if any from the players have combination in the rows
        # If the set contain only 1 value than that value is winner
        if len(set(board[row_idx])) == 1 and board[row_idx][0] != EMPTY:
            return board[row_idx][0]

        # Check if any from the players have combination in the columns
        # If the set contain only 1 value than that value is winner
        if len(set(vertical_list[row_idx])) == 1 and vertical_list[row_idx][0] != EMPTY:
            return vertical_list[row_idx][0]

        # Creating set with values in the diagonals
        # Create diagonal [0][0],[1][1],[2][2]
        diagonal_1.add(board[row_idx][row_idx])
        # Create diagonal [0][2],[1][1],[2][0]
        diagonal_2.add(board[row_idx][l_board-1])
        l_board -= 1

    # Check if any from the players have combination in the diagonals
    if len(diagonal_1) == 1:
        winning_player = diagonal_1.pop()
        return winning_player if winning_player != EMPTY else None
    elif len(diagonal_2) == 1:
        winning_player = diagonal_2.pop()
        return winning_player if winning_player != EMPTY else None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # raise NotImplementedError
    if winner(board) or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # raise NotImplementedError
    res = winner(board)
    if res == X:
        return 1
    elif res == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # raise NotImplementedError
    result_action = tuple()
    p = player(board)
    if player(board) == X:
        value = -1
        for act in actions(board):
            new_value = min_value(result(board, act))
            if new_value > value:
                value = new_value
                result_action = act
    elif player(board) == O:
        value = 1
        for act in actions(board):
            new_value = max_value(result(board, act))
            if new_value < value:
                value = new_value
                result_action = act
    return result_action


def min_value(board):
    if terminal(board):
        return utility(board)

    value = 1
    for act in actions(board):
        value = min(value, max_value(result(board, act)))
    return value


def max_value(board):
    if terminal(board):
        return utility(board)

    value = -1
    for act in actions(board):
        value = max(value, min_value(result(board, act)))
    return value
