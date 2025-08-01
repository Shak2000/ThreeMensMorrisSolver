

class ThreeMensMorrisUI {
    constructor() {
        this.selectedCell = null;
        this.gameState = {
            board: [],
            currentPlayer: 'W',
            whiteCount: 0,
            blackCount: 0,
            isPlacementPhase: true,
            winner: null
        };
        this.init();
    }

    async init() {
        this.setupEventListeners();
        // Initialize with no game active
        this.gameState.gameActive = false;
        this.updateButtonVisibility();
        await this.startNewGame();
    }

    setupEventListeners() {
        // Game control buttons
        document.getElementById('newGameBtn').addEventListener('click', () => this.startNewGame());
        document.getElementById('undoBtn').addEventListener('click', () => this.undoMove());
        document.getElementById('restartBtn').addEventListener('click', () => this.restartGame());
        document.getElementById('aiMoveBtn').addEventListener('click', () => this.makeAIMove());
        document.getElementById('newGameAfterVictory').addEventListener('click', () => this.startNewGameAfterVictory());

        // Board click handler
        document.getElementById('gameBoard').addEventListener('click', (e) => {
            if (e.target.classList.contains('board-cell')) {
                this.handleBoardClick(e.target);
            }
        });
    }

    async startNewGame() {
        try {
            await this.apiCall('/start');
            await this.updateGameState();
            this.showMessage('New game started!', 'success');
        } catch (error) {
            this.showMessage('Failed to start new game', 'error');
        }
    }

    async restartGame() {
        try {
            await this.apiCall('/start');
            await this.updateGameState();
            this.showMessage('Game restarted!', 'success');
        } catch (error) {
            this.showMessage('Failed to restart game', 'error');
        }
    }

    async undoMove() {
        try {
            const result = await this.apiCall('/undo');
            if (result.success) {
                await this.updateGameState();
                this.showMessage('Move undone successfully', 'success');
            } else {
                this.showMessage('No moves to undo', 'error');
            }
        } catch (error) {
            this.showMessage('Failed to undo move', 'error');
        }
    }

    async makeAIMove() {
        const depth = parseInt(document.getElementById('depthInput').value);
        if (depth < 1 || depth > 6) {
            this.showMessage('Please enter a valid depth (1-6)', 'error');
            return;
        }

        this.setLoading(true);
        try {
            const result = await this.apiCall(`/get_computer_move?depth=${depth}`);
            if (result.move) {
                const move = result.move;
                if (move.length === 2) {
                    // Placement move
                    const [x, y] = move;
                    const placeResult = await this.apiCall('/place', { x, y });
                    if (placeResult.success) {
                        this.showMessage(`AI placed piece at (${x}, ${y})`, 'success');
                    } else {
                        this.showMessage('AI made invalid placement', 'error');
                    }
                } else {
                    // Movement move
                    const [sx, sy, dx, dy] = move;
                    const moveResult = await this.apiCall('/move', { x: sx, y: sy, nx: dx, ny: dy });
                    if (moveResult.success) {
                        this.showMessage(`AI moved piece from (${sx}, ${sy}) to (${dx}, ${dy})`, 'success');
                    } else {
                        this.showMessage('AI made invalid move', 'error');
                    }
                }
                await this.updateGameState();
            } else {
                this.showMessage('AI could not find a valid move', 'error');
            }
        } catch (error) {
            this.showMessage('Failed to make AI move', 'error');
        } finally {
            this.setLoading(false);
        }
    }

    async handleBoardClick(cell) {
        if (!cell.classList.contains('clickable') && !cell.classList.contains('piece-white') && !cell.classList.contains('piece-black')) {
            return;
        }

        const [x, y] = this.getCellCoordinates(cell);

        if (this.gameState.isPlacementPhase) {
            await this.handlePlacementMove(x, y);
        } else {
            await this.handleMovementMove(x, y);
        }
    }

    async handlePlacementMove(x, y) {
        try {
            const result = await this.apiCall('/place', { x, y });
            if (result.success) {
                await this.updateGameState();
                this.showMessage(`Piece placed at (${x}, ${y})`, 'success');
            } else {
                this.showMessage('Invalid placement. Position may be occupied.', 'error');
            }
        } catch (error) {
            this.showMessage('Failed to place piece', 'error');
        }
    }

    async handleMovementMove(x, y) {
        if (!this.selectedCell) {
            // Select source piece
            if (this.isValidSourcePiece(x, y)) {
                this.selectCell(x, y);
                await this.showValidMoves(x, y);
            } else {
                this.showMessage('Please select your own piece to move', 'error');
            }
        } else {
            // Select destination
            const [sx, sy] = this.getCellCoordinates(this.selectedCell);
            if (this.isValidDestination(x, y, sx, sy)) {
                await this.executeMove(sx, sy, x, y);
            } else {
                this.showMessage('Invalid destination. Must be adjacent and empty.', 'error');
            }
        }
    }

    isValidSourcePiece(x, y) {
        const cell = this.getCellAt(x, y);
        const currentPlayerPiece = this.gameState.currentPlayer === 'W' ? 'piece-white' : 'piece-black';
        return cell && cell.classList.contains(currentPlayerPiece);
    }

    async executeMove(sx, sy, dx, dy) {
        try {
            const result = await this.apiCall('/move', { x: sx, y: sy, nx: dx, ny: dy });
            if (result.success) {
                await this.updateGameState();
                this.showMessage(`Piece moved from (${sx}, ${sy}) to (${dx}, ${dy})`, 'success');
            } else {
                this.showMessage('Invalid move. Check piece ownership and adjacency.', 'error');
            }
        } catch (error) {
            this.showMessage('Failed to move piece', 'error');
        } finally {
            this.clearSelection();
        }
    }



    isValidDestination(x, y, sx, sy) {
        const cell = this.getCellAt(x, y);
        return cell && cell.classList.contains('valid-move');
    }

    selectCell(x, y) {
        this.clearSelection();
        const cell = this.getCellAt(x, y);
        if (cell) {
            cell.classList.add('selected');
            this.selectedCell = cell;
        }
    }

    clearSelection() {
        if (this.selectedCell) {
            this.selectedCell.classList.remove('selected');
            this.selectedCell = null;
        }
        this.clearValidMoves();
    }

    async showValidMoves(sx, sy) {
        try {
            const result = await this.apiCall(`/get_adjacent_positions?x=${sx}&y=${sy}`);
            result.adjacent.forEach(([x, y]) => {
                const cell = this.getCellAt(x, y);
                if (cell && cell.classList.contains('empty')) {
                    cell.classList.add('valid-move');
                }
            });
        } catch (error) {
            console.error('Failed to get adjacent positions:', error);
        }
    }

    clearValidMoves() {
        document.querySelectorAll('.board-cell.valid-move').forEach(cell => {
            cell.classList.remove('valid-move');
        });
    }

    async updateGameState() {
        try {
            const state = await this.apiCall('/get_board_state');
            
            this.gameState = {
                board: state.board,
                currentPlayer: state.current_player,
                whiteCount: state.white_count,
                blackCount: state.black_count,
                isPlacementPhase: state.is_placement_phase,
                winner: state.winner,
                gameActive: state.game_active
            };
            
            this.updateUI();
            this.renderBoard();
            this.updateButtonVisibility();
            
            // Check for game over
            if (state.winner) {
                this.showVictoryMessage(state.winner);
                this.gameState.gameActive = false;
                this.updateButtonVisibility();
            }
        } catch (error) {
            console.error('Failed to update game state:', error);
        }
    }

    updateButtonVisibility() {
        const newGameBtn = document.getElementById('newGameBtn');
        const undoBtn = document.getElementById('undoBtn');
        const restartBtn = document.getElementById('restartBtn');
        const aiMoveBtn = document.getElementById('aiMoveBtn');
        const depthInput = document.getElementById('depthInput');

        if (this.gameState.gameActive) {
            // Game is active - show game controls, hide new game
            newGameBtn.style.display = 'none';
            undoBtn.style.display = 'inline-block';
            restartBtn.style.display = 'inline-block';
            aiMoveBtn.style.display = 'inline-block';
            depthInput.style.display = 'inline-block';
        } else {
            // No game active - show only new game button
            newGameBtn.style.display = 'inline-block';
            undoBtn.style.display = 'none';
            restartBtn.style.display = 'none';
            aiMoveBtn.style.display = 'none';
            depthInput.style.display = 'none';
        }
    }

    updateUI() {
        // Update current player
        const playerName = this.gameState.currentPlayer === 'W' ? 'White' : 'Black';
        document.getElementById('currentPlayer').textContent = playerName;
        
        // Update piece counts
        document.getElementById('whiteCount').textContent = this.gameState.whiteCount;
        document.getElementById('blackCount').textContent = this.gameState.blackCount;
        
        // Update game phase
        const phaseText = this.gameState.isPlacementPhase ? 'Placement Phase' : 'Movement Phase';
        document.getElementById('gamePhase').textContent = phaseText;
    }

    renderBoard() {
        const boardElement = document.getElementById('gameBoard');
        boardElement.innerHTML = '';

        // Create 5x5 grid for the visual board
        const visualBoard = [
            ['*', '─', '*', '─', '*'],
            ['│', '\\', '│', '/', '│'],
            ['*', '─', '*', '─', '*'],
            ['│', '/', '│', '\\', '│'],
            ['*', '─', '*', '─', '*']
        ];

        // Create cells
        for (let row = 0; row < 5; row++) {
            for (let col = 0; col < 5; col++) {
                const cell = document.createElement('div');
                cell.className = 'board-cell';
                
                const char = visualBoard[row][col];
                if (char === '*') {
                    // This is a position where pieces can be placed
                    const [boardX, boardY] = this.getBoardCoordinates(row, col);
                    if (boardX !== null && boardY !== null) {
                        cell.dataset.x = boardX;
                        cell.dataset.y = boardY;
                        cell.classList.add('empty');
                        
                        // Check if this position has a piece
                        const piece = this.gameState.board[boardY]?.[boardX];
                        if (piece === 'W') {
                            cell.classList.remove('empty');
                            cell.classList.add('piece-white');
                            cell.textContent = 'W';
                        } else if (piece === 'B') {
                            cell.classList.remove('empty');
                            cell.classList.add('piece-black');
                            cell.textContent = 'B';
                        } else {
                            cell.classList.add('clickable');
                        }
                    }
                } else {
                    // This is a connection line
                    cell.classList.add('connection');
                    cell.textContent = char;
                }
                
                boardElement.appendChild(cell);
            }
        }
    }

    getBoardCoordinates(visualRow, visualCol) {
        const reverseMap = {
            '0,0': [0, 0], '0,2': [0, 1], '0,4': [0, 2],
            '2,0': [1, 0], '2,2': [1, 1], '2,4': [1, 2],
            '4,0': [2, 0], '4,2': [2, 1], '4,4': [2, 2]
        };
        const key = `${visualRow},${visualCol}`;
        return reverseMap[key] || [null, null];
    }

    getCellCoordinates(cell) {
        return [parseInt(cell.dataset.x), parseInt(cell.dataset.y)];
    }

    getCellAt(x, y) {
        return document.querySelector(`[data-x="${x}"][data-y="${y}"]`);
    }

    getPlayerClass() {
        return this.gameState.currentPlayer === 'W' ? 'white' : 'black';
    }

    showMessage(message, type = 'info') {
        const messageElement = document.getElementById('gameMessage');
        messageElement.textContent = message;
        messageElement.className = `message ${type}`;
        
        // Clear message after 3 seconds
        setTimeout(() => {
            messageElement.textContent = '';
            messageElement.className = 'message';
        }, 3000);
    }

    setLoading(loading) {
        const container = document.querySelector('.container');
        if (loading) {
            container.classList.add('loading');
        } else {
            container.classList.remove('loading');
        }
    }

    showVictoryMessage(winner) {
        const overlay = document.getElementById('victoryOverlay');
        const message = document.getElementById('victoryMessage');
        const winnerName = winner === 'W' ? 'White' : 'Black';
        
        message.textContent = `${winnerName} Wins!`;
        overlay.style.display = 'flex';
    }

    async startNewGameAfterVictory() {
        const overlay = document.getElementById('victoryOverlay');
        overlay.style.display = 'none';
        await this.startNewGame();
    }

    async apiCall(endpoint, data = null) {
        const url = endpoint.startsWith('http') ? endpoint : `http://localhost:8000${endpoint}`;
        
        try {
            if (data) {
                // POST request with data
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                return await response.json();
            } else {
                // GET request
                const response = await fetch(url);
                return await response.json();
            }
        } catch (error) {
            console.error(`API call failed for ${endpoint}:`, error);
            throw error;
        }
    }
}

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ThreeMensMorrisUI();
});
