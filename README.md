# Three Men's Morris Solver

A complete implementation of the classic Three Men's Morris board game with an AI opponent using minimax algorithm with alpha-beta pruning. Features both a web-based GUI and command-line interface.

## 🎮 Game Overview

Three Men's Morris is a strategy board game played on a 3×3 grid with diagonal connections. Players take turns placing and then moving their pieces to form a line of three pieces (horizontally, vertically, or diagonally).

### Game Rules

1. **Placement Phase**: Players alternate placing their 3 pieces on empty positions
2. **Movement Phase**: Once all pieces are placed, players move their pieces to adjacent empty positions
3. **Victory**: First player to form a line of 3 pieces wins
4. **Adjacent Movement**: Pieces can only move to connected positions (including diagonals through the center)

## 🚀 Features

- **Web-based GUI**: Modern, responsive interface with visual board representation
- **AI Opponent**: Minimax algorithm with alpha-beta pruning and configurable difficulty
- **Command-line Interface**: Terminal-based gameplay option
- **Game Controls**: Undo moves, restart games, and step-by-step gameplay
- **Real-time Updates**: Live game state tracking and victory detection
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.7+
- FastAPI
- uvicorn (for web server)

## 🛠️ Installation

1. **Clone or download the project files**:
   ```bash
   # Ensure you have these files:
   # - main.py (game logic)
   # - app.py (web server)
   # - index.html (web interface)
   # - styles.css (styling)
   # - script.js (frontend logic)
   ```

2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn
   ```

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the web server**:
   ```bash
   uvicorn app:app --reload
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

3. **Play the game**:
   - Click "New Game" to start
   - Click on empty positions to place pieces during placement phase
   - Click on your pieces then click destination during movement phase
   - Use "AI Move" button to let the computer play
   - Adjust AI difficulty with the search depth slider (1-6)

### Command Line Interface

Run the game directly in your terminal:

```bash
python main.py
```

Follow the on-screen prompts to:
- Start new games
- Make manual moves
- Let the AI play
- Undo moves
- Restart games

## 🧠 AI Algorithm

The AI uses the **Minimax algorithm with alpha-beta pruning**:

- **Evaluation Function**: 
  - +100,000 for winning positions
  - -100,000 for losing positions
  - +1 for each potential winning line (2 pieces + 1 empty)
  - -1 for each opponent's potential winning line

- **Search Depth**: Configurable from 1-6 levels
  - Depth 1-2: Easy (fast, basic moves)
  - Depth 3-4: Medium (good strategy)
  - Depth 5-6: Hard (strong play, slower)

- **Optimization**: Alpha-beta pruning significantly reduces search space

## 🏗️ Project Structure

```
three-mens-morris/
├── main.py          # Core game logic and CLI
├── app.py           # FastAPI web server
├── index.html       # Web interface HTML
├── styles.css       # Web interface styling
├── script.js        # Frontend JavaScript logic
└── README.md        # This file
```

### Key Components

- **`Game` class** (`main.py`): Core game logic, board state, move validation
- **FastAPI server** (`app.py`): REST API endpoints for web interface
- **Web UI**: Modern, responsive interface with real-time updates
- **AI Engine**: Minimax with alpha-beta pruning for optimal play

## 🎮 Game Controls

### Web Interface
- **New Game**: Start a fresh game
- **Undo Move**: Revert the last move
- **Restart**: Reset current game
- **AI Move**: Let computer play current turn
- **Search Depth**: Adjust AI difficulty (1-6)

### Command Line
- **Manual Action**: Make your own move
- **Computer Action**: Let AI play with custom depth
- **Undo Move**: Revert last move
- **Restart Game**: Start over
- **Quit**: Exit the game

## 🎯 Game Strategy Tips

1. **Control the Center**: The middle position (1,1) connects to all other positions
2. **Block Opponent Lines**: Prevent your opponent from forming lines of 2
3. **Create Multiple Threats**: Set up situations where you can win on the next move
4. **Think Ahead**: Consider your opponent's possible responses
5. **Endgame Planning**: In movement phase, mobility becomes crucial

## 🔧 API Endpoints

The web server provides these REST API endpoints:

- `GET /start` - Start a new game
- `GET /undo` - Undo the last move
- `GET /get_board_state` - Get current game state
- `POST /place` - Place a piece (placement phase)
- `POST /move` - Move a piece (movement phase)
- `GET /get_computer_move?depth=N` - Get AI move suggestion
- `GET /get_adjacent_positions?x=X&y=Y` - Get valid moves from position

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" error**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Web interface not loading**:
   - Ensure the server is running (`uvicorn app:app --reload`)
   - Check that you're accessing `http://localhost:8000`
   - Verify all files (HTML, CSS, JS) are in the same directory

3. **AI taking too long**:
   - Reduce search depth to 3 or lower
   - Higher depths (5-6) require more computation time

4. **Port already in use**:
   ```bash
   uvicorn app:app --reload --port 8001
   ```

## 🤝 Contributing

Feel free to enhance this project! Some ideas:
- Add different board sizes (6 Men's Morris, 9 Men's Morris)
- Implement online multiplayer
- Add move history visualization
- Create mobile app version
- Improve AI evaluation function

## 📝 License

This project is open source and available under the MIT License.

## 🎉 Acknowledgments

- Classic Three Men's Morris game rules
- Minimax algorithm with alpha-beta pruning
- Modern web technologies for the interface

---

Enjoy playing Three Men's Morris! 🎮
