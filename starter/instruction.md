# Sudoku Project Instructions

## Project goals

- Preserve the existing Flask application structure and public API behavior.

- Keep the Sudoku generator working with a strict unique-solution guarantee.

- Support Easy, Medium, and Hard difficulty modes without changing the route contract.

- Keep the frontend usable, responsive, and accessible while maintaining the existing visual style.

## Coding expectations

- Prefer small, reusable functions and clear module boundaries.

- Keep comments focused on non-obvious logic or rubric requirements.

- Do not add unnecessary dependencies or large framework changes.

- Preserve working behavior while improving maintainability and testability.

## Testing requirements

- Use pytest for all automated validation.

- Add or update tests for Sudoku logic, Flask routes, difficulty handling, and invalid game states.

- Verify uniqueness of generated puzzles and keep regression tests focused on real behavior.

- Run the complete suite before concluding work is complete.

## UI and gameplay constraints

- Keep the board responsive for mobile and desktop.

- Preserve alternating 3x3 square coloring and readable controls.

- Prefilled cells must remain locked/read-only.

- Keep game state consistent and handle errors gracefully.

- New Game, timer, hint, difficulty tuning, and leaderboard should all keep working together.

## Safety and project hygiene

- Do not remove required files or screenshots.

- Do not add virtual environments or generated cache directories to the final project state.

- Keep requirements.txt aligned with the libraries actually needed to run and test the app.

## Comments and Documentation

- Comments were added in the Sudoku logic module (`sudoku_logic.py`) to explain puzzle generation, validation, and solution checking logic.

- Comments were added in JavaScript (`main.js`) to describe UI interactions such as timer handling, hint functionality, difficulty changes, and leaderboard updates.

- These comments help future developers understand the purpose of each component and make future modifications easier without breaking existing functionality.

- Code style consistency was maintained by using clear function names, modular functions, consistent formatting, and keeping related logic grouped together.

## Build and Testing Verification

- The application was tested locally by running the Flask application and verifying all gameplay features.

- Automated tests were executed using pytest.

- Final test result: 23 tests passed successfully.

- The refactoring maintained existing Sudoku behavior while improving structure and maintainability.

## How to Run

- From the `starter` directory, create the virtual environment using `py -m venv .venv`.

- Activate the virtual environment using `.venv\Scripts\activate`.

- Install the required dependencies using `py -m pip install -r requirements.txt`.

- Run the Flask application using `py app.py`.

- Open `http://127.0.0.1:5000` in the browser.

## Feature Testing

- Sudoku board: Start a new game and verify that the 9x9 board is displayed correctly.

- Difficulty levels: Select Easy, Medium, and Hard and verify that the number of prefilled cells changes.

- Unique solution: Generate puzzles and verify that each puzzle has exactly one solution.

- Locked cells: Try to edit a prefilled cell and verify that it remains locked.

- Invalid moves: Enter a conflicting value and verify that the invalid cell is highlighted.

- Hint: Click Hint and verify that one correct empty cell is filled and locked.

- Check Solution: Enter an incorrect value and click Check Solution to verify that the incorrect entry is highlighted.

- Timer: Start a new game and verify that the timer runs and stops after the puzzle is solved.

- Completion: Complete the puzzle and verify that the congratulations message appears.

- Leaderboard: Complete a puzzle and verify that the score is saved with the player's name, time, difficulty, and number of hints.

- Local storage: Refresh the browser and verify that the saved score remains in the Top 10 list.

- Dark/Light mode: Toggle between Dark Mode and Light Mode and verify that the UI changes correctly.

- 3x3 styling: Verify that the Sudoku 3x3 boxes have alternating styling.

- Responsive layout: Resize the browser window and verify that the game remains usable on smaller screens.

## Copilot Prompts Used

- Testing framework: Set up pytest and create baseline tests for the existing Flask Sudoku project without changing application behavior.

- Unique solution: Implement Sudoku generation with exactly one unique solution and add tests to verify uniqueness.

- Difficulty levels: Add Easy, Medium, and Hard difficulty levels with different numbers of prefilled cells.

- Invalid moves: Add immediate visual feedback for row, column, and 3x3 box conflicts.

- Hint: Add a Hint button that fills one correct empty cell and locks the cell.

- Check Solution: Add a Check Solution button that highlights incorrect entries.

- Timer and completion: Add a solve timer and show a congratulations message when the puzzle is completed.

- Leaderboard: Implement a Top 10 scoreboard using browser localStorage with the player's name, time, difficulty, and number of hints used.

- Theme and styling: Add Dark Mode and Light Mode, alternating 3x3 box styling, and responsive layout.

- Board rendering: Fix the Sudoku board rendering issue while preserving the existing functionality.

## Copilot Suggestion Review

- Copilot suggestions were reviewed before they were accepted.

- During testing, one generated test for a 3x3 box conflict used incorrect cell coordinates. The test was corrected so that the conflicting value was placed in the same 3x3 box as the tested cell.

- The application logic was not changed just to make an incorrect test pass.

- Changes were accepted after checking that they matched the project requirements and that the tests passed.