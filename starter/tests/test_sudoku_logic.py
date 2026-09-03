import sudoku_logic


def is_valid_board(board):
    expected = set(range(1, sudoku_logic.SIZE + 1))
    rows = [set(row) for row in board]
    columns = [
        {board[row][column] for row in range(sudoku_logic.SIZE)}
        for column in range(sudoku_logic.SIZE)
    ]
    boxes = [
        {
            board[row][column]
            for row in range(box_row, box_row + 3)
            for column in range(box_column, box_column + 3)
        }
        for box_row in range(0, sudoku_logic.SIZE, 3)
        for box_column in range(0, sudoku_logic.SIZE, 3)
    ]
    return all(group == expected for group in rows + columns + boxes)


def test_create_empty_board_has_expected_shape_and_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1

    assert not sudoku_logic.is_safe(board, 0, 1, 1)
    assert not sudoku_logic.is_safe(board, 1, 0, 1)
    assert not sudoku_logic.is_safe(board, 1, 1, 1)
    assert sudoku_logic.is_safe(board, 1, 1, 2)


def test_is_valid_move_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[1][1] = 2
    board[0][1] = 3

    assert not sudoku_logic.is_valid_move(board, 0, 1, 1)
    assert not sudoku_logic.is_valid_move(board, 1, 0, 2)
    assert not sudoku_logic.is_valid_move(board, 1, 2, 3)
    assert sudoku_logic.is_valid_move(board, 1, 2, 4)


def test_is_valid_move_rejects_occupied_and_out_of_range_cells():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1

    assert not sudoku_logic.is_valid_move(board, 0, 0, 1)
    assert not sudoku_logic.is_valid_move(board, 0, 1, 0)
    assert not sudoku_logic.is_valid_move(board, 0, 1, 10)


def test_is_complete_detects_exact_solution_match():
    solution = sudoku_logic.create_empty_board()
    solution[0][0] = 1
    board = sudoku_logic.deep_copy(solution)

    assert sudoku_logic.is_complete(board, solution)
    board[0][1] = 2
    assert not sudoku_logic.is_complete(board, solution)


def test_fill_board_creates_a_valid_solution():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board)
    assert is_valid_board(board)


def test_count_solutions_identifies_unique_puzzle():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=35)

    assert sudoku_logic.count_solutions(puzzle) == 1


def test_count_solutions_returns_zero_for_invalid_puzzle():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 1

    assert sudoku_logic.count_solutions(board) == 0


def test_count_solutions_stops_at_two_for_multiple_solutions():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(board) == 2


def test_generate_puzzle_preserves_solution_values_and_clue_count():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert is_valid_board(solution)
    assert sudoku_logic.count_solutions(puzzle) == 1
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert all(
        puzzle[row][column] in (sudoku_logic.EMPTY, solution[row][column])
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )


def test_deep_copy_does_not_mutate_original_board():
    board = sudoku_logic.create_empty_board()
    copied_board = sudoku_logic.deep_copy(board)
    copied_board[0][0] = 9

    assert board[0][0] == sudoku_logic.EMPTY
