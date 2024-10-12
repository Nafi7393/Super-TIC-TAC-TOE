SMALL_GRID_SIZE = 3
GRID_SIZE = 9


# Initialize game state
def initialize_game_state():
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    small_boards = [[None for _ in range(SMALL_GRID_SIZE)] for _ in range(SMALL_GRID_SIZE)]
    next_grid = None  # Next grid to play in
    winner = None
    game_over = False
    current_player = 'X'  # 'X' always starts
    return {
        'board': board,
        'small_boards': small_boards,
        'next_grid': next_grid,
        'winner': winner,
        'game_over': game_over,
        'current_player': current_player,
    }


# Check if a small board is won
def check_small_board_win(board, small_grid_row, small_grid_col, player):
    small_board = [
        [
            board[r][c]
            for c in range(small_grid_col * SMALL_GRID_SIZE, (small_grid_col + 1) * SMALL_GRID_SIZE)
        ]
        for r in range(small_grid_row * SMALL_GRID_SIZE, (small_grid_row + 1) * SMALL_GRID_SIZE)
    ]

    # Check rows and columns
    for i in range(SMALL_GRID_SIZE):
        if all(cell == player for cell in small_board[i]):
            return True
        if all(row[i] == player for row in small_board):
            return True

    # Check diagonals
    if all(small_board[i][i] == player for i in range(SMALL_GRID_SIZE)):
        return True
    if all(small_board[i][SMALL_GRID_SIZE - i - 1] == player for i in range(SMALL_GRID_SIZE)):
        return True

    return False


# Check if the super grid is won
def check_super_grid_win(small_boards, player):
    # Check rows and columns
    for i in range(SMALL_GRID_SIZE):
        if all(cell == player for cell in small_boards[i]):
            return True
        if all(row[i] == player for row in small_boards):
            return True

    # Check diagonals
    if all(small_boards[i][i] == player for i in range(SMALL_GRID_SIZE)):
        return True
    if all(small_boards[i][SMALL_GRID_SIZE - i - 1] == player for i in range(SMALL_GRID_SIZE)):
        return True

    return False


# Check if the game is a draw
def check_draw(small_boards):
    return all(all(cell is not None for cell in row) for row in small_boards)


# Make a move on the board
def make_move(board, small_boards, row, col, current_player):
    small_grid_row, small_grid_col = row // SMALL_GRID_SIZE, col // SMALL_GRID_SIZE
    small_row, small_col = row % SMALL_GRID_SIZE, col % SMALL_GRID_SIZE

    # Place the move
    board[row][col] = current_player

    # Check if the player won the small board
    if check_small_board_win(board, small_grid_row, small_grid_col, current_player):
        # Mark the small board as won
        small_boards[small_grid_row][small_grid_col] = current_player

        # Fill the small board with the player's symbol
        for r in range(small_grid_row * SMALL_GRID_SIZE, (small_grid_row + 1) * SMALL_GRID_SIZE):
            for c in range(small_grid_col * SMALL_GRID_SIZE, (small_grid_col + 1) * SMALL_GRID_SIZE):
                board[r][c] = current_player

    # Determine the next grid based on the move
    next_grid = (small_row, small_col)

    # If the next grid is already won or full, free play
    if (
        small_boards[small_row][small_col] is not None
        or is_small_board_full(board, small_row, small_col)
    ):
        next_grid = None

    return next_grid


# Check if a small grid is full
def is_small_board_full(board, grid_row, grid_col):
    for r in range(grid_row * SMALL_GRID_SIZE, (grid_row + 1) * SMALL_GRID_SIZE):
        for c in range(grid_col * SMALL_GRID_SIZE, (grid_col + 1) * SMALL_GRID_SIZE):
            if board[r][c] is None:
                return False
    return True


# Save game state to a file
def save_game_state(game_state, filename='savegame.dat'):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(game_state, f)


# Load game state from a file
def load_game_state(filename='savegame.dat'):
    import pickle
    with open(filename, 'rb') as f:
        game_state = pickle.load(f)
    return game_state


# Reset the game state
def reset_game_state():
    return initialize_game_state()


