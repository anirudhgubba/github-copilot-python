# Copilot Instructions

## Project
This is a Python Flask Sudoku game. The application should remain modular,
readable, maintainable, and easy to test.

## Core Requirements
- Generate valid Sudoku puzzles with exactly one unique solution.
- Support Easy, Medium, and Hard difficulty levels.
- Keep prefilled cells locked.
- Provide immediate feedback for invalid moves and conflicts.
- Provide Hint and Check functionality.
- Track solving time.
- Show a congratulatory message when the puzzle is completed.
- Store the Top 10 scores in browser localStorage.
- Support dark and light themes.
- Use alternating styling for the 3x3 Sudoku boxes.
- Make the UI responsive for desktop and mobile.

## Code Style
- Use modern Python compatible with Python 3.13.
- Prefer small, reusable functions.
- Use clear variable and function names.
- Add type hints where appropriate.
- Avoid unnecessary global state.
- Keep game logic separate from Flask routes and presentation.
- Add comments/docstrings where they improve understanding.
- Preserve existing functionality unless a requirement specifically changes it.

## Testing
- Use pytest for automated tests.
- Run tests after every significant change.
- Do not modify application behavior just to make a test pass.
- Add tests for important Sudoku logic and application features.

## Frontend
- Keep HTML, CSS, and JavaScript organized and maintainable.
- Ensure controls and text remain readable in both themes.
- Use accessible labels and clear visual feedback.
- Ensure the layout works on desktop and mobile.

## Important
Before implementing a feature, inspect the existing code and reuse suitable
components instead of unnecessarily rewriting working code.