import math
import copy
from game_functions import SMALL_GRID_SIZE, GRID_SIZE, is_small_board_full, check_draw, check_super_grid_win

INF = math.inf


def check_small_board_win(small_board):
    # Check rows and columns
    for i in range(SMALL_GRID_SIZE):
        if small_board[i][0] == small_board[i][1] == small_board[i][2] and small_board[i][0] is not None:
            return small_board[i][0]
        if small_board[0][i] == small_board[1][i] == small_board[2][i] and small_board[0][i] is not None:
            return small_board[0][i]

    # Check diagonals
    if small_board[0][0] == small_board[1][1] == small_board[2][2] and small_board[0][0] is not None:
        return small_board[0][0]
    if small_board[0][2] == small_board[1][1] == small_board[2][0] and small_board[0][2] is not None:
        return small_board[0][2]

    return None


def update_small_board(board, small_boards, grid_row, grid_col):
    small_board = [[board[r][c] for c in range(grid_col * SMALL_GRID_SIZE, (grid_col + 1) * SMALL_GRID_SIZE)]
                   for r in range(grid_row * SMALL_GRID_SIZE, (grid_row + 1) * SMALL_GRID_SIZE)]

    winner = check_small_board_win(small_board)
    if winner:
        small_boards[grid_row][grid_col] = winner


def set_difficulty(difficulty):
    if difficulty == 'easy':
        return 1
    elif difficulty == 'medium':
        return 3
    elif difficulty == 'hard':
        return 5
    else:
        return 3  # Default to medium


class AIPlayer:
    def __init__(self, symbol, difficulty='medium'):
        self.symbol = symbol  # 'X' or 'O'
        self.opponent = 'O' if self.symbol == 'X' else 'X'
        self.difficulty = difficulty
        self.max_depth = set_difficulty(difficulty)

    def make_move(self, board, small_boards, next_grid):
        best_score = -INF
        best_move = None

        if next_grid is None:
            # AI can play in any available small grid
            grids_to_consider = []
            for grid_row in range(SMALL_GRID_SIZE):
                for grid_col in range(SMALL_GRID_SIZE):
                    if small_boards[grid_row][grid_col] is None:
                        grids_to_consider.append((grid_row, grid_col))
        else:
            grids_to_consider = [next_grid]

        for grid_row, grid_col in grids_to_consider:
            for r in range(grid_row * SMALL_GRID_SIZE, (grid_row + 1) * SMALL_GRID_SIZE):
                for c in range(grid_col * SMALL_GRID_SIZE, (grid_col + 1) * SMALL_GRID_SIZE):
                    if board[r][c] is None:
                        # Simulate the move
                        board_copy = copy.deepcopy(board)
                        small_boards_copy = copy.deepcopy(small_boards)
                        board_copy[r][c] = self.symbol

                        # Update small boards if necessary
                        update_small_board(board_copy, small_boards_copy, grid_row, grid_col)

                        # Determine next grid
                        next_small_row = r % SMALL_GRID_SIZE
                        next_small_col = c % SMALL_GRID_SIZE
                        next_grid_next = (next_small_row, next_small_col)
                        if small_boards_copy[next_small_row][next_small_col] is not None or \
                           is_small_board_full(board_copy, next_small_row, next_small_col):
                            next_grid_next = None

                        score = self.minimax(board_copy, small_boards_copy, self.max_depth - 1, False, -INF, INF, next_grid_next)
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
        return best_move

    def minimax(self, board, small_boards, depth, is_maximizing, alpha, beta, next_grid):
        if depth == 0 or self.is_terminal_state(small_boards):
            return self.evaluate(board, small_boards)

        if next_grid is None:
            # Can play in any grid
            grids_to_consider = []
            for grid_row in range(SMALL_GRID_SIZE):
                for grid_col in range(SMALL_GRID_SIZE):
                    if small_boards[grid_row][grid_col] is None:
                        grids_to_consider.append((grid_row, grid_col))
        else:
            grids_to_consider = [next_grid]

        if is_maximizing:
            max_eval = -INF
            for grid_row, grid_col in grids_to_consider:
                for r in range(grid_row * SMALL_GRID_SIZE, (grid_row + 1) * SMALL_GRID_SIZE):
                    for c in range(grid_col * SMALL_GRID_SIZE, (grid_col + 1) * SMALL_GRID_SIZE):
                        if board[r][c] is None:
                            # Simulate the move
                            board_copy = copy.deepcopy(board)
                            small_boards_copy = copy.deepcopy(small_boards)
                            board_copy[r][c] = self.symbol

                            # Update small boards if necessary
                            update_small_board(board_copy, small_boards_copy, grid_row, grid_col)

                            # Determine next grid
                            next_small_row = r % SMALL_GRID_SIZE
                            next_small_col = c % SMALL_GRID_SIZE
                            next_grid_next = (next_small_row, next_small_col)
                            if small_boards_copy[next_small_row][next_small_col] is not None or \
                               is_small_board_full(board_copy, next_small_row, next_small_col):
                                next_grid_next = None

                            eval = self.minimax(board_copy, small_boards_copy, depth - 1, False, alpha, beta, next_grid_next)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
                else:
                    continue
                break
            return max_eval
        else:
            min_eval = INF
            for grid_row, grid_col in grids_to_consider:
                for r in range(grid_row * SMALL_GRID_SIZE, (grid_row + 1) * SMALL_GRID_SIZE):
                    for c in range(grid_col * SMALL_GRID_SIZE, (grid_col + 1) * SMALL_GRID_SIZE):
                        if board[r][c] is None:
                            # Simulate the move
                            board_copy = copy.deepcopy(board)
                            small_boards_copy = copy.deepcopy(small_boards)
                            board_copy[r][c] = self.opponent

                            # Update small boards if necessary
                            update_small_board(board_copy, small_boards_copy, grid_row, grid_col)

                            # Determine next grid
                            next_small_row = r % SMALL_GRID_SIZE
                            next_small_col = c % SMALL_GRID_SIZE
                            next_grid_next = (next_small_row, next_small_col)
                            if small_boards_copy[next_small_row][next_small_col] is not None or \
                               is_small_board_full(board_copy, next_small_row, next_small_col):
                                next_grid_next = None

                            eval = self.minimax(board_copy, small_boards_copy, depth - 1, True, alpha,
                                                beta, next_grid_next)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
                else:
                    continue
                break
            return min_eval

    def evaluate(self, board, small_boards):
        # Heuristic evaluation function
        score = 0

        # Evaluate super grid
        score += self.evaluate_super_grid(small_boards)

        # Evaluate small boards
        for grid_row in range(SMALL_GRID_SIZE):
            for grid_col in range(SMALL_GRID_SIZE):
                if small_boards[grid_row][grid_col] is None:
                    small_board = [[board[r][c] for c in range(grid_col * SMALL_GRID_SIZE, (grid_col + 1) * SMALL_GRID_SIZE)]
                                   for r in range(grid_row * SMALL_GRID_SIZE, (grid_row + 1) * SMALL_GRID_SIZE)]
                    score += self.evaluate_small_board(small_board)
                else:
                    if small_boards[grid_row][grid_col] == self.symbol:
                        score += 50  # AI controls this small board
                    else:
                        score -= 50  # Opponent controls this small board

        return score

    def evaluate_super_grid(self, small_boards):
        score = 0
        # Rows
        for row in range(SMALL_GRID_SIZE):
            row_cells = small_boards[row]
            score += self.evaluate_line(row_cells)

        # Columns
        for col in range(SMALL_GRID_SIZE):
            col_cells = [small_boards[row][col] for row in range(SMALL_GRID_SIZE)]
            score += self.evaluate_line(col_cells)

        # Diagonals
        diag1 = [small_boards[i][i] for i in range(SMALL_GRID_SIZE)]
        diag2 = [small_boards[i][SMALL_GRID_SIZE - i - 1] for i in range(SMALL_GRID_SIZE)]
        score += self.evaluate_line(diag1)
        score += self.evaluate_line(diag2)

        return score * 100  # Weight super grid more heavily

    def evaluate_small_board(self, small_board):
        score = 0
        # Rows
        for row in small_board:
            score += self.evaluate_line(row)

        # Columns
        for col in range(SMALL_GRID_SIZE):
            col_cells = [small_board[row][col] for row in range(SMALL_GRID_SIZE)]
            score += self.evaluate_line(col_cells)

        # Diagonals
        diag1 = [small_board[i][i] for i in range(SMALL_GRID_SIZE)]
        diag2 = [small_board[i][SMALL_GRID_SIZE - i - 1] for i in range(SMALL_GRID_SIZE)]
        score += self.evaluate_line(diag1)
        score += self.evaluate_line(diag2)

        return score

    def evaluate_line(self, line):
        score = 0
        if line.count(self.symbol) == 3:
            score += 100
        elif line.count(self.symbol) == 2 and line.count(None) == 1:
            score += 10
        elif line.count(self.symbol) == 1 and line.count(None) == 2:
            score += 1

        if line.count(self.opponent) == 3:
            score -= 100
        elif line.count(self.opponent) == 2 and line.count(None) == 1:
            score -= 10
        elif line.count(self.opponent) == 1 and line.count(None) == 2:
            score -= 1

        return score

    def is_terminal_state(self, small_boards):
        return check_super_grid_win(small_boards, self.symbol) or \
               check_super_grid_win(small_boards, self.opponent) or \
               check_draw(small_boards)



