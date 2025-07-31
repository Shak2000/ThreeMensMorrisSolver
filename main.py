class Game:
    visual = [
        "*─*─*",
        "|\\|/|",
        "*─*─*",
        "|\\|/|",
        "*─*─*"
    ]

    def __init__(self):
        self.board = [['*' for j in range(3)] for i in range(3)]
        self.player = 'W'
        self.white = 0
        self.black = 0
        self.history = []

    def start(self):
        self.board = [['*' for j in range(3)] for i in range(3)]
        self.player = 'W'
        self.white = 0
        self.black = 0
        self.history = []

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
            return True
        return False

    def move(self, x, y, nx, ny):
        if (self.white == 3 and self.black == 3 and 0 <= x < 3 and 0 <= y < 3 and 0 <= nx < 3 and 0 <= ny < 3
                and self.board[y][x] == self.player and self.board[ny][nx] == '*'):
            self.history.append([[self.board[i][j] for j in range(3)] for i in range(3)])
            self.board[y][x] = '*'
            self.board[ny][nx] = self.player
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


def main():
    print("Welcome to the Three Men's Morris Solver!")


if __name__ == "__main__":
    main()
