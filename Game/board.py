class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def place_move(self, row, col, player):
        self.board[row][col] = player

    def undo_move(self, row, col):
        self.board[row][col] = 0

    def is_empty(self, row, col):
        return self.board[row][col] == 0

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def copy(self):
        return [row[:] for row in self.board]