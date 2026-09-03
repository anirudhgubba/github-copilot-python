import pytest

import app
import sudoku_logic


@pytest.fixture()
def client():
    app.app.config.update(TESTING=True)
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    with app.app.test_client() as test_client:
        yield test_client
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None


def test_index_renders_game_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data
    assert b'sudoku-board' in response.data
    assert b'Top 10 Scores' in response.data
    assert b'player-name' in response.data
    assert b'theme-toggle' in response.data


def test_new_game_returns_requested_number_of_clues(client):
    response = client.get('/new?clues=40')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert sum(cell != 0 for row in puzzle for cell in row) == 40
    assert app.CURRENT['solution'] is not None


@pytest.mark.parametrize(
    ('difficulty', 'expected_clues'),
    [('easy', 45), ('medium', 35), ('hard', 30)],
)
def test_new_game_difficulty_controls_unique_clue_count(
    client, difficulty, expected_clues
):
    response = client.get(f'/new?difficulty={difficulty}')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert sum(cell != 0 for row in puzzle for cell in row) == expected_clues
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_new_game_rejects_unknown_difficulty(client):
    response = client.get('/new?difficulty=expert')

    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid difficulty'}


def test_hint_fills_one_empty_cell_with_correct_value_and_locks_it(client):
    client.get('/new?clues=40')
    empty_cells = [
        (row, col)
        for row in range(9)
        for col in range(9)
        if app.CURRENT['puzzle'][row][col] == 0
    ]
    row, col = empty_cells[0]

    response = client.post('/hint', json={'row': row, 'col': col})

    assert response.status_code == 200
    assert response.get_json() == {
        'row': row,
        'col': col,
        'value': app.CURRENT['solution'][row][col],
        'locked': True,
    }


def test_hint_does_not_overwrite_prefilled_cell(client):
    client.get('/new?clues=40')
    filled_cell = next(
        (row, col)
        for row in range(9)
        for col in range(9)
        if app.CURRENT['puzzle'][row][col] != 0
    )

    response = client.post('/hint', json={'row': filled_cell[0], 'col': filled_cell[1]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'Cell is already filled'}


def test_check_without_active_game_returns_error(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_solution_identifies_incorrect_cells(client):
    new_game_response = client.get('/new')
    solution = new_game_response.get_json()['puzzle']
    solution = [row[:] for row in app.CURRENT['solution']]
    solution[0][0] = (solution[0][0] % 9) + 1

    response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == [[0, 0]]


def test_check_solution_ignores_empty_cells(client):
    client.get('/new?clues=40')
    solution = app.CURRENT['solution']
    row, col = next(
        (row, col)
        for row in range(9)
        for col in range(9)
        if app.CURRENT['puzzle'][row][col] == 0
    )
    board = [[0] * 9 for _ in range(9)]
    board[row][col] = (solution[row][col] % 9) + 1

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [[row, col]], 'solved': False}


def test_check_solution_accepts_current_solution(client):
    client.get('/new')

    response = client.post('/check', json={'board': app.CURRENT['solution']})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [], 'solved': True}
