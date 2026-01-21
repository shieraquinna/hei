// Sudoku Game Logic
class SudokuGame {
    constructor() {
        this.board = [];
        this.originalBoard = [];
        this.solution = [];
        this.startTime = null;
        this.timerInterval = null;
        this.difficulty = null;
    }

    // Generate a valid Sudoku puzzle
    generatePuzzle(difficulty) {
        this.difficulty = difficulty;
        
        // Generate solved board
        this.solution = this.generateSolvedBoard();
        
        // Remove numbers based on difficulty
        const cellsToRemove = {
            'easy': 64,    // 17 clues
            'medium': 73,  // 8 clues (lebih banyak removed)
            'hard': 78     // 3 clues (paling banyak removed, tapi untuk level hard kita pakai 7-8)
        };

        // Untuk ease of play, kami adjust numbers
        const removeCounts = {
            'easy': 64,    // Keep 17 clues
            'medium': 73,  // Keep 8 clues
            'hard': 82     // Keep 7-8 clues
        };

        this.board = JSON.parse(JSON.stringify(this.solution));
        this.originalBoard = JSON.parse(JSON.stringify(this.solution));
        
        let removed = 0;
        const targetRemove = removeCounts[difficulty];

        for (let i = 0; i < 81 && removed < targetRemove; i++) {
            const row = Math.floor(i / 9);
            const col = i % 9;
            
            if (this.board[row][col] !== 0) {
                const backup = this.board[row][col];
                this.board[row][col] = 0;
                
                // Check if puzzle still has unique solution
                if (this.countSolutions(JSON.parse(JSON.stringify(this.board))) === 1) {
                    this.originalBoard[row][col] = 0;
                    removed++;
                } else {
                    this.board[row][col] = backup;
                }
            }
        }
    }

    generateSolvedBoard() {
        const board = Array(9).fill().map(() => Array(9).fill(0));
        this.fillBoard(board);
        return board;
    }

    fillBoard(board) {
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (board[row][col] === 0) {
                    const numbers = this.shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9]);
                    
                    for (let num of numbers) {
                        if (this.isValid(board, row, col, num)) {
                            board[row][col] = num;
                            
                            if (this.fillBoard(board)) {
                                return true;
                            }
                            
                            board[row][col] = 0;
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }

    isValid(board, row, col, num) {
        // Check row
        for (let i = 0; i < 9; i++) {
            if (board[row][i] === num) return false;
        }

        // Check column
        for (let i = 0; i < 9; i++) {
            if (board[i][col] === num) return false;
        }

        // Check 3x3 box
        const boxRow = Math.floor(row / 3) * 3;
        const boxCol = Math.floor(col / 3) * 3;
        for (let i = boxRow; i < boxRow + 3; i++) {
            for (let j = boxCol; j < boxCol + 3; j++) {
                if (board[i][j] === num) return false;
            }
        }

        return true;
    }

    shuffle(array) {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    countSolutions(board, count = [0]) {
        if (count[0] > 1) return count[0];

        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (board[row][col] === 0) {
                    for (let num = 1; num <= 9; num++) {
                        if (this.isValid(board, row, col, num)) {
                            board[row][col] = num;
                            this.countSolutions(board, count);
                            board[row][col] = 0;
                        }
                    }
                    return count[0];
                }
            }
        }

        count[0]++;
        return count[0];
    }

    isComplete() {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.board[i][j] === 0) return false;
            }
        }
        return true;
    }

    isSolved() {
        if (!this.isComplete()) return false;

        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.board[i][j] !== this.solution[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }

    getHint() {
        const emptyCells = [];
        
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.board[i][j] === 0 && this.originalBoard[i][j] === 0) {
                    emptyCells.push({row: i, col: j, value: this.solution[i][j]});
                }
            }
        }

        if (emptyCells.length === 0) return null;

        const hint = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        this.board[hint.row][hint.col] = hint.value;
        
        return hint;
    }
}

// Global game instance
let game = new SudokuGame();
let currentHints = 0;

// Start the game
function startGame(difficulty) {
    game.generatePuzzle(difficulty);
    currentHints = 0;
    
    document.querySelector('.level-selector').style.display = 'none';
    document.getElementById('boardContainer').style.display = 'flex';
    
    const levelNames = {
        'easy': 'Mudah ⭐',
        'medium': 'Sedang ⭐⭐',
        'hard': 'Sulit ⭐⭐⭐'
    };
    
    document.getElementById('levelDisplay').textContent = levelNames[difficulty];
    
    renderBoard();
    startTimer();
}

// Render the Sudoku board
function renderBoard() {
    const table = document.getElementById('sudokuBoard');
    table.innerHTML = '';

    for (let i = 0; i < 9; i++) {
        const row = document.createElement('tr');
        
        for (let j = 0; j < 9; j++) {
            const cell = document.createElement('td');
            const input = document.createElement('input');
            
            input.id = `cell-${i}-${j}`;
            input.type = 'text';
            input.maxLength = '1';
            input.value = game.board[i][j] || '';
            
            if (game.originalBoard[i][j] !== 0) {
                input.classList.add('given');
                input.disabled = true;
            } else {
                input.addEventListener('input', (e) => handleInput(e, i, j));
                input.addEventListener('focus', () => highlightRelated(i, j));
            }
            
            cell.appendChild(input);
            row.appendChild(cell);
        }
        
        table.appendChild(row);
    }
}

// Handle input in cells
function handleInput(e, row, col) {
    let value = e.target.value;

    // Only allow numbers 1-9
    if (value !== '' && (value < '1' || value > '9')) {
        e.target.value = '';
        return;
    }

    game.board[row][col] = value ? parseInt(value) : 0;
    
    // Remove error styling
    e.target.classList.remove('error');

    // Check for duplicates in real-time
    checkForDuplicates(row, col);
}

// Check for duplicate numbers
function checkForDuplicates(row, col) {
    const value = game.board[row][col];
    
    if (value === 0) return;

    // Check row
    for (let j = 0; j < 9; j++) {
        if (j !== col && game.board[row][j] === value) {
            document.getElementById(`cell-${row}-${col}`).classList.add('error');
            document.getElementById(`cell-${row}-${j}`).classList.add('error');
            return;
        }
    }

    // Check column
    for (let i = 0; i < 9; i++) {
        if (i !== row && game.board[i][col] === value) {
            document.getElementById(`cell-${row}-${col}`).classList.add('error');
            document.getElementById(`cell-${i}-${col}`).classList.add('error');
            return;
        }
    }

    // Check 3x3 box
    const boxRow = Math.floor(row / 3) * 3;
    const boxCol = Math.floor(col / 3) * 3;
    for (let i = boxRow; i < boxRow + 3; i++) {
        for (let j = boxCol; j < boxCol + 3; j++) {
            if ((i !== row || j !== col) && game.board[i][j] === value) {
                document.getElementById(`cell-${row}-${col}`).classList.add('error');
                document.getElementById(`cell-${i}-${j}`).classList.add('error');
                return;
            }
        }
    }
}

// Highlight related cells
function highlightRelated(row, col) {
    // Clear previous highlights
    document.querySelectorAll('.sudoku-board input').forEach(input => {
        input.classList.remove('selected', 'related');
    });

    // Highlight selected cell
    document.getElementById(`cell-${row}-${col}`).classList.add('selected');

    // Highlight cells in same row
    for (let j = 0; j < 9; j++) {
        if (j !== col) {
            document.getElementById(`cell-${row}-${j}`).classList.add('related');
        }
    }

    // Highlight cells in same column
    for (let i = 0; i < 9; i++) {
        if (i !== row) {
            document.getElementById(`cell-${i}-${col}`).classList.add('related');
        }
    }

    // Highlight cells in same 3x3 box
    const boxRow = Math.floor(row / 3) * 3;
    const boxCol = Math.floor(col / 3) * 3;
    for (let i = boxRow; i < boxRow + 3; i++) {
        for (let j = boxCol; j < boxCol + 3; j++) {
            if (i !== row || j !== col) {
                document.getElementById(`cell-${i}-${j}`).classList.add('related');
            }
        }
    }
}

// Give hint
function giveHint() {
    const hint = game.getHint();
    const hintDisplay = document.getElementById('hintDisplay');
    
    if (hint) {
        currentHints++;
        hintDisplay.textContent = `💡 Hint ${currentHints}: Baris ${hint.row + 1}, Kolom ${hint.col + 1} = ${hint.value}`;
        
        const input = document.getElementById(`cell-${hint.row}-${hint.col}`);
        input.value = hint.value;
        input.disabled = true;
        input.classList.add('given');
    } else {
        hintDisplay.textContent = 'Tidak ada sel kosong untuk hint!';
    }
}

// Clear user inputs
function clearBoard() {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            if (game.originalBoard[i][j] === 0) {
                game.board[i][j] = 0;
                const input = document.getElementById(`cell-${i}-${j}`);
                input.value = '';
                input.classList.remove('error');
            }
        }
    }
    
    document.getElementById('hintDisplay').textContent = '';
    currentHints = 0;
}

// Check solution
function checkSolution() {
    const hintDisplay = document.getElementById('hintDisplay');
    
    if (!game.isComplete()) {
        hintDisplay.textContent = '⚠️ Silakan isi semua kotak terlebih dahulu!';
        hintDisplay.style.backgroundColor = '#ffcccc';
        hintDisplay.style.borderLeftColor = '#c00';
        setTimeout(() => {
            hintDisplay.textContent = '';
            hintDisplay.style.backgroundColor = '';
            hintDisplay.style.borderLeftColor = '';
        }, 3000);
        return;
    }

    if (game.isSolved()) {
        stopTimer();
        showWinModal();
    } else {
        hintDisplay.textContent = '❌ Ada yang salah! Periksa kembali jawaban Anda.';
        hintDisplay.style.backgroundColor = '#ffcccc';
        hintDisplay.style.borderLeftColor = '#c00';
    }
}

// Timer functions
function startTimer() {
    game.startTime = Date.now();
    
    if (game.timerInterval) clearInterval(game.timerInterval);
    
    game.timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - game.startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        
        document.getElementById('timer').textContent = 
            `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
}

function stopTimer() {
    if (game.timerInterval) clearInterval(game.timerInterval);
}

// Show level selector
function showLevelSelector() {
    stopTimer();
    document.getElementById('boardContainer').style.display = 'none';
    document.querySelector('.level-selector').style.display = 'block';
    document.getElementById('levelDisplay').textContent = '-';
    document.getElementById('timer').textContent = '00:00';
    document.getElementById('winModal').style.display = 'none';
    document.getElementById('hintDisplay').textContent = '';
}

// Win modal
function showWinModal() {
    const timeDisplay = document.getElementById('timer').textContent;
    document.getElementById('finalTime').textContent = timeDisplay;
    document.getElementById('winModal').style.display = 'flex';
}

// Rules modal
function showRules() {
    document.getElementById('rulesModal').style.display = 'flex';
}

function closeRules() {
    document.getElementById('rulesModal').style.display = 'none';
}

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    const winModal = document.getElementById('winModal');
    const rulesModal = document.getElementById('rulesModal');
    
    if (e.target === winModal) {
        winModal.style.display = 'none';
    }
    if (e.target === rulesModal) {
        rulesModal.style.display = 'none';
    }
});
