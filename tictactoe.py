"""
Tic Tac Toe Player
"""


import copy
import math


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

    X_count = 0      # Counter for the number of 'X' symbols on the board
    O_count = 0      # Counter for the number of 'O' symbols on the board
    EMPTY_count = 0  # Counter for the number of empty cells on the board

    # Loop through each row in the board:
    for row in board:
        # Count the number of 'X' symbols in the current row
        X_count += row.count(X)
        # Count the number of 'O' symbols in the current row
        O_count += row.count(O)
        # Count the number of empty cells in the current row
        EMPTY_count += row.count(EMPTY)

    # If X has more squares than O, its O's turn:
    if X_count > O_count:
        return O

    # Otherwise it is X's turn:
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (x, y) available on the board.

    x represents the board row, y the board column, both 0, 1 or 2

    The actions are represented as the tuple (x, y) where the piece can be placed.
    """

    possible_moves = set()  # Create an empty set to store possible moves

    for x in range(3):  # Iterate through (represents) rows (0, 1, 2)
        for y in range(3):  # Iterate through (represents) columns (0, 1, 2)
            if board[x][y] == EMPTY:  # If the cell is empty
                possible_moves.add((x, y))  # Add the move to the set

    return possible_moves  # Return the set of all possible moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    x, y = action  # Unpack the action into row and column indices

    # Check if the move is valid:
    if not (0 <= x < 3 and 0 <= y < 3):
        raise ValueError("Invalid action: Invalid board position")

    if board[x][y] != EMPTY:
        raise ValueError("Invalid action: Cell is already occupied")

    # Create a deep copy of the board to avoid modifying the original board:
    new_board = copy.deepcopy(board)

    # Update the copied board with the current player's move:
    new_board[x][y] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for p in [X, O]:
        # Check rows and columns
        for x in range(3):
            if all(cell == p for cell in board[x]) or all(board[y][x] == p for y in range(3)):
                return p

        # Check diagonals
        if all(board[x][x] == p for x in range(3)) or all(board[x][2 - x] == p for x in range(3)):
            return p

    return None  # Return None if no winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is over if it is a winning board or all tiles are full (no actions):

    if winner(board) or not any(EMPTY in row for row in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1  # X has won, utility is 1
    elif winner(board) == "O":
        return -1  # O has won, utility is -1
    else:
        return 0  # Game ended in a tie, utility is 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    'X' Player is trying to maximise the score, 'O' Player is trying to minimise it
    """
    if terminal(board):
        return None  # If the game is over, return None as there's no move to make

    if player(board) == X:
        # Initialize best value as negative infinity for maximization
        best_value = -math.inf
        best_move = None  # Initialize best move as None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value  # Update best_value
                best_move = action  # Update best_move
    else:
        # Initialize best value as positive infinity for minimization
        best_value = math.inf
        best_move = None  # Initialize best move as None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value  # Update best_value
                best_move = action  # Update best_move

    return best_move  # Return the best move found


def max_value(board):
    if terminal(board):
        return utility(board)  # Return utility for terminal state

    v = -math.inf  # Initialize v as negative infinity

    for action in actions(board):
        # Update v by selecting the maximum value
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)  # Return utility for terminal state

    v = math.inf  # Initialize v as positive infinity

    for action in actions(board):
        # Update v by selecting the minimum value
        v = min(v, max_value(result(board, action)))

    return v
