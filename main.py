import copy
import math


class Game:
    visual = [
        "*─*─*",
        "|\\|/|",
        "*─*─*",
        "|/|\\|",
        "*─*─*"
    ]

    adjacent = {
        (0, 0): [(0, 1), (1, 0), (1, 1)],
        (0, 1): [(0, 0), (0, 2), (1, 1)],
        (0, 2): [(0, 1), (1, 1), (1, 2)],
        (1, 0): [(0, 0), (2, 0), (1, 1)],
        (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
        (1, 2): [(0, 2), (1, 1), (2, 2)],
        (2, 0): [(1, 0), (1, 1), (2, 1)],
        (2, 1): [(1, 1), (2, 0), (2, 2)],
        (2, 2): [(1, 1), (1, 2), (2, 1)]
    }

    lines = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    def __init__(self):
        self.board = [['*' for j in range(3)] for i in range(3)]
        self.player = 'W'
        self.white = 0
        self.black = 0
        self.history = []
        self.game_active = False

    def start(self):
        self.board = [['*' for j in range(3)] for i in range(3)]
        self.player = 'W'
        self.white = 0
        self.black = 0
        self.history = []
        self.game_active = True

    def switch(self):
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

    def place(self, x, y):
        if self.black < 3 and 0 <= x < 3 and 0 <= y < 3 and self.board[y][x] == '*':
            self.history.append([[self.board[i][j] for j in range(3)] for i in range(3)])
            self.board[y][x] = self.player
            if self.player == 'W':
                self.white += 1
            else:
                self.black += 1
            self.switch()
            return True
        return False

    def move(self, x, y, nx, ny):
        if (self.white == 3 and self.black == 3 and 0 <= x < 3 and 0 <= y < 3 and 0 <= nx < 3 and 0 <= ny < 3
                and self.board[y][x] == self.player and self.board[ny][nx] == '*'
                and (nx, ny) in self.adjacent[(x, y)]):
            self.history.append([[self.board[i][j] for j in range(3)] for i in range(3)])
            self.board[y][x] = '*'
            self.board[ny][nx] = self.player
            self.switch()
            return True
        return False

    def undo(self):
        if self.history:
            self.board = self.history.pop()
            # Recalculate piece counts
            self.white = sum(1 for row in self.board for cell in row if cell == 'W')
            self.black = sum(1 for row in self.board for cell in row if cell == 'B')
            # Switch back to previous player
            self.switch()
            return True
        return False

    def get_winner(self):
        # This function checks if a player has formed a line of 3
        for line in self.lines:
            p1, p2, p3 = line
            if (self.board[p1[1]][p1[0]] != '*' and
                    self.board[p1[1]][p1[0]] == self.board[p2[1]][p2[0]] == self.board[p3[1]][p3[0]]):
                return self.board[p1[1]][p1[0]]
        return None

    def display_board(self):
        print("\nCurrent Board:")
        visual_board = [list(row) for row in self.visual]
        
        coord_map = {
            (0, 0): (0, 0), (0, 1): (0, 2), (0, 2): (0, 4),
            (1, 0): (2, 0), (1, 1): (2, 2), (1, 2): (2, 4),
            (2, 0): (4, 0), (2, 1): (4, 2), (2, 2): (4, 4)
        }

        for y in range(3):
            for x in range(3):
                if self.board[y][x] != '*':
                    vis_y, vis_x = coord_map[(x, y)]
                    visual_board[vis_y][vis_x] = self.board[y][x]
        
        for row in visual_board:
            print("  " + "".join(row))
        
        print(f"\nCurrent Player: {'White' if self.player == 'W' else 'Black'}")
        print(f"White pieces: {self.white}/3, Black pieces: {self.black}/3")
        print("Legend: W = White, B = Black, * = Empty")

    def is_placement_phase(self):
        return self.white < 3 or self.black < 3

    def is_move_phase(self):
        return self.white == 3 and self.black == 3

    def evaluate_board(self):
        """
        Evaluates the current board state.
        - +100 for White win, -100 for Black win.
        - +10 for each unblocked 2-in-a-row for White.
        - -10 for each unblocked 2-in-a-row for Black.
        """
        winner = self.get_winner()
        if winner == 'W':
            return 100000
        if winner == 'B':
            return -100000

        score = 0
        for line in self.lines:
            pieces = [self.board[p[1]][p[0]] for p in line]
            if pieces.count('W') == 2 and pieces.count('*') == 1:
                score += 1
            elif pieces.count('B') == 2 and pieces.count('*') == 1:
                score -= 1
        return score

    def get_possible_moves(self):
        """
        Gets all possible moves for the current player.
        Returns a list of moves. For placement, a move is (x, y).
        For movement, a move is (from_x, from_y, to_x, to_y).
        """
        moves = []
        if self.is_placement_phase():
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == '*':
                        moves.append((x, y))
        else: # Movement phase
            my_pieces = []
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == self.player:
                        my_pieces.append((x, y))
            
            for x, y in my_pieces:
                for nx, ny in self.adjacent[(x, y)]:
                    if self.board[ny][nx] == '*':
                        moves.append((x, y, nx, ny))
        return moves

    def minimax(self, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or self.get_winner() is not None:
            return self.evaluate_board()

        possible_moves = self.get_possible_moves()

        if maximizing_player:
            max_eval = -math.inf
            for move in possible_moves:
                # Create a copy and execute the move
                child_game = copy.deepcopy(self)
                if len(move) == 2:
                    child_game.place(move[0], move[1])
                else:
                    child_game.move(move[0], move[1], move[2], move[3])
                
                evaluation = child_game.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break # Prune
            return max_eval
        else: # Minimizing player
            min_eval = math.inf
            for move in possible_moves:
                child_game = copy.deepcopy(self)
                if len(move) == 2:
                    child_game.place(move[0], move[1])
                else:
                    child_game.move(move[0], move[1], move[2], move[3])

                evaluation = child_game.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break # Prune
            return min_eval

    def get_computer_move(self, depth):
        """
        Finds the best move for the computer using minimax.
        """
        best_move = None
        possible_moves = self.get_possible_moves()
        
        if self.player == 'W': # Maximizer
            best_val = -math.inf
            for move in possible_moves:
                child_game = copy.deepcopy(self)
                if len(move) == 2:
                    child_game.place(move[0], move[1])
                else:
                    child_game.move(move[0], move[1], move[2], move[3])
                
                move_val = child_game.minimax(depth - 1, -math.inf, math.inf, False)
                if move_val > best_val:
                    best_val = move_val
                    best_move = move
        else: # Minimizer
            best_val = math.inf
            for move in possible_moves:
                child_game = copy.deepcopy(self)
                if len(move) == 2:
                    child_game.place(move[0], move[1])
                else:
                    child_game.move(move[0], move[1], move[2], move[3])

                move_val = child_game.minimax(depth - 1, -math.inf, math.inf, True)
                if move_val < best_val:
                    best_val = move_val
                    best_move = move
        
        return best_move


def main():
    def get_valid_coordinates(prompt):
        """Get valid x,y coordinates from user input"""
        while True:
            try:
                coords = input(prompt).strip().split()
                if len(coords) != 2:
                    print("Error: Please enter exactly two numbers (x y)")
                    continue
                x, y = int(coords[0]), int(coords[1])
                if 0 <= x <= 2 and 0 <= y <= 2:
                    return x, y
                else:
                    print("Error: Coordinates must be between 0 and 2")
            except ValueError:
                print("Error: Please enter valid numbers")
    
    print("Welcome to the Three Men's Morris Solver!")
    game = Game()
    
    while True:
        if not game.game_active:
            print("\n" + "="*40)
            print("1. Start a new game")
            print("2. Quit")
            print("="*40)
            
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == "1":
                game.start()
                print("New game started!")
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        else:
            game.display_board()
            
            winner = game.get_winner()
            if winner:
                print(f"\n🎉 {'White' if winner == 'W' else 'Black'} wins! 🎉")
                game.game_active = False
                continue
            
            print("\n" + "="*40)
            print("1. Take a manual action")
            print("2. Let computer take an action")
            print("3. Undo a move")
            print("4. Restart the game")
            print("5. Quit")
            print("="*40)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                if game.is_placement_phase():
                    print(f"\nPlacement phase - {game.player} to place a piece")
                    x, y = get_valid_coordinates("Enter coordinates (x y): ")
                    if not game.place(x, y):
                        print("Error: Invalid placement. Position may be occupied or out of bounds.")
                else:
                    print(f"\nMovement phase - {game.player} to move a piece")
                    src_x, src_y = get_valid_coordinates("Enter source coordinates (x y): ")
                    dst_x, dst_y = get_valid_coordinates("Enter destination coordinates (x y): ")
                    if not game.move(src_x, src_y, dst_x, dst_y):
                        print("Error: Invalid move. Check piece ownership, adjacency, and destination.")
                            
            elif choice == "2":
                # Computer takes an action
                depth = 0
                while True:
                    try:
                        depth_str = input("Enter minimax search depth (e.g., 3): ").strip()
                        depth = int(depth_str)
                        if depth > 0:
                            break
                        else:
                            print("Error: Depth must be a positive integer.")
                    except ValueError:
                        print("Error: Please enter a valid integer for the depth.")

                print(f"Computer is thinking with depth {depth}...")
                move = game.get_computer_move(depth)

                if move is None:
                    print("Computer could not find a valid move.")
                elif len(move) == 2: # Placement move
                    x, y = move
                    print(f"Computer places a piece at ({x}, {y})")
                    game.place(x, y)
                else: # Movement move
                    sx, sy, dx, dy = move
                    print(f"Computer moves a piece from ({sx}, {sy}) to ({dx}, {dy})")
                    game.move(sx, sy, dx, dy)

            elif choice == "3":
                if game.undo():
                    print("Move undone successfully")
                else:
                    print("Error: No moves to undo")
                    
            elif choice == "4":
                game.start()
                print("Game restarted!")
                
            elif choice == "5":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
