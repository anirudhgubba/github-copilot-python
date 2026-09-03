# Flask Sudoku Game

This project is a Flask-based Sudoku game. It generates puzzles with unique solutions, lets players choose a difficulty, validates entries as they are made, and provides hints and solution checking in the browser.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.13 or later
- A modern web browser such as Chrome, Edge, or Firefox

### Installation

1. Fork this repository to your GitHub account. (You can use the "Fork" button on the top right corner of the repository page.)

2. Clone your forked repository to your local machine.

3. Open PowerShell and navigate to the `starter` directory.

4. Create and activate a Python virtual environment on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell script execution is restricted, activate the environment from Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

5. Install required Python packages.

```powershell
py -m pip install -r requirements.txt
```

6. Run the Flask app.

```powershell
py app.py
```

7. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Run Tests

From the `starter` directory, run the full pytest suite:

```powershell
py -m pytest
```

## Implemented Features

- Unique-solution Sudoku puzzle generation.
- Easy, Medium, and Hard difficulty levels with different clue counts.
- Locked prefilled cells and immediate row, column, and 3x3 box conflict validation.
- Hints that fill and lock one correct cell at a time.
- Check functionality that identifies incorrect entries without overwriting them.
- Solve timer that starts with each puzzle and stops on exact completion.
- Completion message and browser-local Top 10 scoreboard, sorted by fastest time.
- Persistent light/dark theme selection, alternating 3x3 box styling, and responsive desktop/mobile layout.

## Project Instructions

Use GitHub Copilot to refactor the code for this game to add more advanced features. The goal is to create a more modern and maintainable codebase and add additional functionality to the final product. You can use any combination of code completion and chat features, like Ask, Edit, or Agent modes.

- Errors should be handled gracefully with appropriate messages to the user.
- Implement a Sudoku board generator that creates a valid Sudoku puzzle with a unique solution.
- Add a timer to track how long it takes to solve the puzzle.
- Implement a solution checker that verifies if the user's solution is correct using event delegation.
- Add a difficulty selector to allow users to choose between easy, medium, and hard puzzles.
- Add a hint feature that provides clues for the user that are noted with unique colors.
- Add a check puzzle button that checks the current state of the board against the solution.
- User should get immediate feedback on their input, such as highlighting invalid entries.
- Top 10 scores should be saved in local storage and displayed on the page with the user's name, time taken, hints used, and difficulty level.
- The game should be responsive and work well on both desktop and mobile devices.
- UI colors should be visually appealing and accessible.
- Completed and correct puzzles should display a congratulatory message with the time taken and hints used and ask for the user's name for Top 10 times.
