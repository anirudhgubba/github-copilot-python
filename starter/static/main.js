// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const SCORE_STORAGE_KEY = 'sudokuTopScores';
const THEME_STORAGE_KEY = 'sudokuTheme';
let puzzle = [];
let timerInterval = null;
let timerStartedAt = null;
let elapsedSeconds = 0;
let hintsUsed = 0;

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('dark-theme', isDark);
  const toggle = document.getElementById('theme-toggle');
  toggle.innerText = isDark ? 'Light Mode' : 'Dark Mode';
  toggle.setAttribute('aria-pressed', isDark.toString());
}

function loadTheme() {
  try {
    return localStorage.getItem(THEME_STORAGE_KEY) === 'dark' ? 'dark' : 'light';
  } catch (error) {
    return 'light';
  }
}

function toggleTheme() {
  const theme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
  applyTheme(theme);
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch (error) {
    // Continue using the selected theme for the current page.
  }
}

function formatElapsedTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function updateTimer() {
  if (timerStartedAt === null) return;
  elapsedSeconds = Math.floor((Date.now() - timerStartedAt) / 1000);
  document.getElementById('timer').innerText = formatElapsedTime(elapsedSeconds);
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  timerStartedAt = Date.now();
  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
  updateTimer();
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  timerStartedAt = null;
}

function loadScores() {
  try {
    const storedScores = localStorage.getItem(SCORE_STORAGE_KEY);
    const scores = JSON.parse(storedScores || '[]');
    if (!Array.isArray(scores)) return [];
    return scores
      .filter((score) => score &&
        typeof score.name === 'string' &&
        typeof score.time === 'number' && Number.isFinite(score.time) &&
        typeof score.difficulty === 'string' &&
        typeof score.hints === 'number' && Number.isFinite(score.hints))
      .sort((first, second) => first.time - second.time)
      .slice(0, 10);
  } catch (error) {
    return [];
  }
}

function renderScoreboard() {
  const scoreboard = document.getElementById('scoreboard-list');
  const scores = loadScores();
  scoreboard.innerHTML = '';
  if (!scores.length) {
    const emptyMessage = document.createElement('li');
    emptyMessage.innerText = 'No scores yet.';
    scoreboard.appendChild(emptyMessage);
    return;
  }
  scores.forEach((score) => {
    const entry = document.createElement('li');
    entry.innerText = `${score.name} - ${formatElapsedTime(score.time)} - ` +
      `${score.difficulty} - ${score.hints} hint${score.hints === 1 ? '' : 's'}`;
    scoreboard.appendChild(entry);
  });
}

function saveScore() {
  const nameInput = document.getElementById('player-name');
  const name = nameInput.value.trim();
  const message = document.getElementById('message');
  if (!name) {
    message.style.color = '#d32f2f';
    message.innerText = 'Enter your name to save the score.';
    return;
  }

  const score = {
    name,
    time: elapsedSeconds,
    difficulty: document.getElementById('difficulty').value,
    hints: hintsUsed
  };
  const scores = [...loadScores(), score]
    .sort((first, second) => first.time - second.time)
    .slice(0, 10);
  try {
    localStorage.setItem(SCORE_STORAGE_KEY, JSON.stringify(scores));
    renderScoreboard();
    document.getElementById('completion-form').hidden = true;
    nameInput.value = '';
    message.style.color = '#388e3c';
    message.innerText = 'Score saved!';
  } catch (error) {
    message.style.color = '#d32f2f';
    message.innerText = 'Unable to save the score on this browser.';
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      if ((Math.floor(i / 3) + Math.floor(j / 3)) % 2 === 1) {
        input.classList.add('box-shaded');
      }
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        updateCellValidation(e.target);
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function getCurrentBoard() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let row = 0; row < SIZE; row++) {
    board[row] = [];
    for (let col = 0; col < SIZE; col++) {
      const value = inputs[row * SIZE + col].value;
      board[row][col] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

function isValidMove(board, row, col, value) {
  if (!value) return true;
  for (let index = 0; index < SIZE; index++) {
    if (index !== col && board[row][index] === value) return false;
    if (index !== row && board[index][col] === value) return false;
  }
  const boxRow = Math.floor(row / 3) * 3;
  const boxCol = Math.floor(col / 3) * 3;
  for (let boxOffsetRow = 0; boxOffsetRow < 3; boxOffsetRow++) {
    for (let boxOffsetCol = 0; boxOffsetCol < 3; boxOffsetCol++) {
      const conflictRow = boxRow + boxOffsetRow;
      const conflictCol = boxCol + boxOffsetCol;
      if ((conflictRow !== row || conflictCol !== col) &&
          board[conflictRow][conflictCol] === value) {
        return false;
      }
    }
  }
  return true;
}

function updateCellValidation(input) {
  const row = Number(input.dataset.row);
  const col = Number(input.dataset.col);
  const value = input.value ? parseInt(input.value, 10) : 0;
  input.classList.remove('valid', 'invalid');
  if (!value) return;
  input.classList.add(isValidMove(getCurrentBoard(), row, col, value) ? 'valid' : 'invalid');
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      inp.className = 'sudoku-cell';
      if ((Math.floor(i / 3) + Math.floor(j / 3)) % 2 === 1) {
        inp.classList.add('box-shaded');
      }
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  stopTimer();
  hintsUsed = 0;
  document.getElementById('completion-form').hidden = true;
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  startTimer();
}

async function requestHint() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const emptyCells = Array.from(inputs).filter((input) => !input.disabled && !input.value);
  if (!emptyCells.length) return;

  const input = emptyCells[0];
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      row: Number(input.dataset.row),
      col: Number(input.dataset.col)
    })
  });
  const data = await res.json();
  if (data.error) return;
  input.value = data.value;
  input.disabled = data.locked;
  input.className = 'sudoku-cell hinted';
  hintsUsed += 1;
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getCurrentBoard();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('valid', 'invalid', 'incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    } else if (inp.value) {
      inp.classList.add('valid');
    }
  }
  if (data.solved) {
    stopTimer();
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
    document.getElementById('completion-form').hidden = false;
    document.getElementById('player-name').focus();
  } else if (incorrect.size === 0) {
    msg.style.color = '#333';
    msg.innerText = 'Keep going!';
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  applyTheme(loadTheme());
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('completion-form').addEventListener('submit', (event) => {
    event.preventDefault();
    saveScore();
  });
  renderScoreboard();
  // initialize
  newGame();
});