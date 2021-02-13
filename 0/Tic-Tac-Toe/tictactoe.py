"""
Tic Tac Toe Player
"""

import math, copy

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
    c1, c2 = 0, 0   #counts
    if board == initial_state:
        return X
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == X:
                    c1 =  c1 + 1
                elif board[i][j] == O:
                    c2 = c2 + 1
        if c1 > c2:
            return O
        else:
            return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    act = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                act.append((i,j))
    return act


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action[0], action[1]
    if board[i][j] == EMPTY:
        pl = player(board)
        AuxBoard = copy.deepcopy(board)
        AuxBoard[i][j] = pl
        return AuxBoard
    else:
        raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if SearchPat(board, X) == X:
        return X
    elif SearchPat(board, O) == O:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    if player(board) == X:
        val = -50
        move = None
        for action in actions(board):
            valaux = MinValue(result(board, action))
            if valaux >= val:
                val =  valaux
                move = action
        return move
    if player(board) == O:
        val = 50
        move = None
        for action in actions(board):
            valaux = MaxValue(result(board, action))
            if valaux <= val:
                val =  valaux
                move = action
        return move

def SearchPat(board, Letter):
    if board[0][0] == Letter:
        if board[0][1] == Letter and board[0][2] == Letter:
            return Letter
        elif board[1][0] == Letter and board[2][0] == Letter:
            return Letter
        elif board[1][1] == Letter and board[2][2] == Letter:
            return Letter
    if board[0][1] == Letter:
        if board[1][1] == Letter and board[2][1] == Letter:
            return Letter
    if board[0][2] == Letter:
        if board[1][2] == Letter and board[2][2] == Letter:
            return Letter
    if board[1][0] == Letter:
        if board[1][1] == Letter and board[1][2] == Letter: 
            return Letter
    if board[2][0] == Letter:
        if board[2][1] == Letter and board[2][2] == Letter:
            return Letter
        elif board[1][1] == Letter and board[0][2] == Letter:
            return Letter
    else:
        return None

def MaxValue(board):
    if terminal(board) == True:
        return utility(board)
    v = -50
    for action in actions(board):
        v = max(v, MinValue(result(board, action)))
    return v
def MinValue(board):
    if terminal(board) == True:
        return utility(board)
    v = 50
    for action in actions(board):
        v = min(v, MaxValue(result(board, action)))
    return v