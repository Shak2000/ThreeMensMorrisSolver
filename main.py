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
        if self.board[0][0] != '*' and (self.board[0][0] == self.board[0][1] == self.board[0][2]
                                        or self.board[0][0] == self.board[1][0] == self.board[2][0]
                                        or self.board[0][0] == self.board[1][1] == self.board[2][2]):
            return self.board[0][0]
        if self.board[1][0] != '*' and self.board[1][0] == self.board[1][1] == self.board[1][2]:
            return self.board[1][0]
        if self.board[2][0] != '*' and (self.board[2][0] == self.board[1][1] == self.board[0][2]
                                        or self.board[2][0] == self.board[2][1] == self.board[2][2]):
            return self.board[2][0]
        if self.board[0][1] != '*' and self.board[0][1] == self.board[1][1] == self.board[2][1]:
            return self.board[0][1]
        if self.board[0][2] != '*' and self.board[0][2] == self.board[1][2] == self.board[2][2]:
            return self.board[0][2]
        return None

    def display_board(self):
        print("\nCurrent Board:")
        # Create a visual representation using the template
        visual_board = []
        for i in range(5):
            visual_board.append(list(self.visual[i]))
        
        # Place pieces on the visual board
        # Map board coordinates to visual positions
        # Top row: positions 0,0 -> visual[0][0], 0,1 -> visual[0][2], 0,2 -> visual[0][4]
        # Middle row: positions 1,0 -> visual[2][0], 1,1 -> visual[2][2], 1,2 -> visual[2][4]
        # Bottom row: positions 2,0 -> visual[4][0], 2,1 -> visual[4][2], 2,2 -> visual[4][4]
        
        # Top row
        if self.board[0][0] != '*':
            visual_board[0][0] = self.board[0][0]
        if self.board[0][1] != '*':
            visual_board[0][2] = self.board[0][1]
        if self.board[0][2] != '*':
            visual_board[0][4] = self.board[0][2]
        
        # Middle row
        if self.board[1][0] != '*':
            visual_board[2][0] = self.board[1][0]
        if self.board[1][1] != '*':
            visual_board[2][2] = self.board[1][1]
        if self.board[1][2] != '*':
            visual_board[2][4] = self.board[1][2]
        
        # Bottom row
        if self.board[2][0] != '*':
            visual_board[4][0] = self.board[2][0]
        if self.board[2][1] != '*':
            visual_board[4][2] = self.board[2][1]
        if self.board[2][2] != '*':
            visual_board[4][4] = self.board[2][2]
        
        # Display the visual board
        for row in visual_board:
            print("  " + "".join(row))
        
        print(f"\nCurrent Player: {'White' if self.player == 'W' else 'Black'}")
        print(f"White pieces: {self.white}/3, Black pieces: {self.black}/3")
        print("Legend: W = White, B = Black, * = Empty")

    def is_placement_phase(self):
        return self.white < 3 or self.black < 3

    def is_move_phase(self):
        return self.white == 3 and self.black == 3


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
            # No game being played
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
            # Game is being played
            game.display_board()
            
            # Check for winner
            winner = game.get_winner()
            if winner:
                print(f"\n🎉 {'White' if winner == 'W' else 'Black'} wins! 🎉")
                game.game_active = False
                continue
            
            print("\n" + "="*40)
            print("1. Take an action")
            print("2. Undo a move")
            print("3. Restart the game")
            print("4. Quit")
            print("="*40)
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                # Take an action
                if game.is_placement_phase():
                    # Placement phase
                    print(f"\nPlacement phase - {game.player} to place a piece")
                    x, y = get_valid_coordinates("Enter coordinates (x y): ")
                    
                    if game.place(x, y):
                        print(f"Piece placed at ({x}, {y})")
                    else:
                        print("Error: Invalid placement. Position may be occupied or out of bounds.")
                else:
                    # Movement phase
                    print(f"\nMovement phase - {game.player} to move a piece")
                    print("Enter source coordinates (x y): ")
                    src_x, src_y = get_valid_coordinates("Source: ")
                    print("Enter destination coordinates (x y): ")
                    dst_x, dst_y = get_valid_coordinates("Destination: ")
                    
                    if game.move(src_x, src_y, dst_x, dst_y):
                        print(f"Piece moved from ({src_x}, {src_y}) to ({dst_x}, {dst_y})")
                    else:
                        print("Error: Invalid move. Check that source has your piece and destination is empty.")
                            
            elif choice == "2":
                # Undo a move
                if game.undo():
                    print("Move undone successfully")
                else:
                    print("Error: No moves to undo")
                    
            elif choice == "3":
                # Restart the game
                game.start()
                print("Game restarted!")
                
            elif choice == "4":
                # Quit
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
