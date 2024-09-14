class Rules:
    def check_winner(self, board, row, col, player):
        board_matrix = board.get_board()
        return self.check_direction(board_matrix, row, col, player, 1, 0) or \
            self.check_direction(board_matrix, row, col, player, 0, 1) or \
            self.check_direction(board_matrix, row, col, player, 1, 1) or \
            self.check_direction(board_matrix, row, col, player, 1, -1)

    def check_direction(self, board, row, col, player, d_row, d_col):
        count = 1
        count += self.count_in_direction(board, row, col, player, d_row, d_col)
        count += self.count_in_direction(board, row, col, player, -d_row, -d_col)
        return count >= 5

    def count_in_direction(self, board, row, col, player, d_row, d_col):
        count = 0
        r, c = row + d_row, col + d_col
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            count += 1
            r += d_row
            c += d_col
        return count

    def is_game_over(self, board, player):
        board_matrix = board.get_board()
        for row in range(len(board_matrix)):
            for col in range(len(board_matrix[0])):
                if board_matrix[row][col] == player:
                    if self.check_winner(board, row, col, player):
                        return True
        return False
