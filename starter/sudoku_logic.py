import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def is_valid_move(board, row, col, num):
    """Return whether ``num`` can be placed at an otherwise empty cell."""
    if not 0 <= row < SIZE or not 0 <= col < SIZE or not 1 <= num <= SIZE:
        return False
    if board[row][col] != EMPTY:
        return False
    board_without_cell = deep_copy(board)
    board_without_cell[row][col] = EMPTY
    return is_safe(board_without_cell, row, col, num)


def is_complete(board, solution):
    """Return whether every cell in a board matches the expected solution."""
    return all(
        board[row][col] == solution[row][col]
        for row in range(SIZE)
        for col in range(SIZE)
    )


def count_solutions(board, limit=2):
    """Return the number of solutions found, stopping once ``limit`` is reached."""
    if limit < 1:
        return 0
    working_board = deep_copy(board)
    solution_count = 0

    for row in range(SIZE):
        for col in range(SIZE):
            value = working_board[row][col]
            if value == EMPTY:
                continue
            if not 1 <= value <= SIZE:
                return 0
            working_board[row][col] = EMPTY
            if not is_safe(working_board, row, col, value):
                return 0
            working_board[row][col] = value

    def search():
        nonlocal solution_count
        if solution_count >= limit:
            return

        best_cell = None
        best_candidates = None
        for row in range(SIZE):
            for col in range(SIZE):
                if working_board[row][col] != EMPTY:
                    continue
                candidates = [
                    number
                    for number in range(1, SIZE + 1)
                    if is_safe(working_board, row, col, number)
                ]
                if not candidates:
                    return
                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_cell = (row, col)
                    best_candidates = candidates

        if best_cell is None:
            solution_count += 1
            return

        row, col = best_cell
        for candidate in best_candidates:
            working_board[row][col] = candidate
            search()
            working_board[row][col] = EMPTY
            if solution_count >= limit:
                return

    search()
    return solution_count


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def remove_cells(board, clues):
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    for row, col in cells:
        if sum(cell != EMPTY for current_row in board for cell in current_row) <= clues:
            break
        value = board[row][col]
        if value == EMPTY:
            continue
        board[row][col] = EMPTY
        if count_solutions(board) != 1:
            board[row][col] = value

def generate_puzzle(clues=35):
    if not 0 < clues <= SIZE * SIZE:
        raise ValueError('clues must be between 1 and 81')

    while True:
        solution = create_empty_board()
        fill_board(solution)
        puzzle = deep_copy(solution)
        remove_cells(puzzle, clues)
        if sum(cell != EMPTY for row in puzzle for cell in row) == clues:
            return puzzle, solution
