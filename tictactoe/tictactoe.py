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
    xCount = 0
    oCount = 0

    for row in board:
        xCount += row.count(X)
        oCount += row.count(O)

    if xCount <= oCount:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_moves = set()

    for row_index, row in enumerate(board):
        for column_index, val in enumerate(row):
            if val == None:
                possible_moves.add((row_index, column_index))
    
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = player(board)

    new_board = deepcopy(board)
    i, j = action

    if board[i][j] != None:
        raise Exception
    else:
        new_board[i][j] = player_move

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X, O):
        # check vertical
            for row in board:
                if row == [player] * 3:
                    return player

        # check horizontal
            for i in range(3):
                column = [board[x][i] for x in range(3)]
                if column == [player] * 3:
                    return player
        
        # check diagonal
            if [board[i][i] for i in range(0, 3)] == [player] * 3:
                return player

            elif [board[i][~i] for i in range(0, 3)] == [player] * 3:
                return player
    return None
                               

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is won by one of the players
    if winner(board) != None:
        return True

    # moves still possible
    for row in board:
        if EMPTY in row:
            return False

    # no possible moves
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winCondition = winner(board)

    if winCondition == X:
        return 1
    elif winCondition == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board):
        bestMove = ()
        if terminal(board):
            return utility(board), bestMove
        else:
            v = -5
            for action in actions(board):
                minValue = min_value(result(board, action))[0]
                if minValue > v:
                    v = minValue
                    bestMove = action
            return v, bestMove

    def min_value(board):
        bestValue = ()
        if terminal(board):
            return utility(board), bestValue
        else:
            v = 5
            for action in actions(board):
                maxValue = max_value(result(board, action))[0]
                if maxValue < v:
                    v = maxValue
                    bestValue = action
            return v, bestValue

    currentTurn = player(board)

    if terminal(board):
        return None

    if currentTurn == X:
        return max_value(board)[1]

    else:
        return min_value(board)[1]
