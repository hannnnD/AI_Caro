class MinimaxAI:
    def __init__(self, player, rules, first_player_move, max_depth=10):
        self.player = player
        self.opponent = 3 - player
        self.rules = rules
        self.first_player_move = first_player_move
        self.player_moves = [first_player_move]
        self.ai_moves = []
        self.max_depth = max_depth

    def get_move(self, board):
        best_move = None
        best_score = float('-inf')

        possible_moves = self.get_possible_moves(board)
        if not possible_moves:
            print("No valid moves found.")
            return None

        for row, col in possible_moves:
            if self.rules.check_winner(board, row, col, self.player):
                return row, col
            if self.rules.check_winner(board, row, col, self.opponent):
                return row, col

            board.place_move(row, col, self.player)
            score = self.evaluate_strategic_move(board, row, col)
            board.undo_move(row, col)

            if score > best_score:
                best_score = score
                best_move = (row, col)

        self.ai_moves.append(best_move)
        return best_move

    def get_first_move(self, board):
        center_row, center_col = board.rows // 2, board.cols // 2
        candidates = [(center_row, center_col),
                      (center_row - 1, center_col - 1),
                      (center_row - 1, center_col + 1),
                      (center_row + 1, center_col - 1),
                      (center_row + 1, center_col + 1)]

        for row, col in candidates:
            if board.is_empty(row, col):
                return row, col

        return self.get_possible_moves(board)[0]

    def evaluate_strategic_move(self, board, row, col):
        score = 0

        # Strongly prefer winning moves
        if self.rules.check_winner(board, row, col, self.player):
            return 800

        # Block opponent's winning moves
        if self.rules.check_winner(board, row, col, self.opponent):
            return 1200

        # Enhance recognition of double-threats (Double three, double two, etc.)
        if self.detect_double_threat(board, row, col, self.opponent):
            return 1000  # Prioritize blocking opponent's double threat

        # Offensive evaluation: How much does this move help AI's position
        score += self.evaluate_position(board, row, col, self.player)

        # Defensive evaluation: How much does this move weaken opponent's position
        score += self.evaluate_position(board, row, col, self.opponent) * 0.8

        return score

    def detect_double_threat(self, board, row, col, player):
        threat_count = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # right, down, diagonal-down-right, diagonal-down-left

        # For each direction, check for lines of two or three for the player
        for d_row, d_col in directions:
            count = self.count_line(board, row, col, player, d_row, d_col)

            if count == 2:  # Two-in-a-row in this direction
                threat_count += 1
            elif count == 3:  # Three-in-a-row in this direction
                threat_count += 1

            # If there are two separate lines (double threat), return True
            if threat_count >= 2:
                return True

        return False

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if depth == self.max_depth or self.rules.is_game_over(board, self.player) or self.rules.is_game_over(board, self.opponent):
            return self.evaluate_board(board)

        if is_maximizing:
            max_eval = float('-inf')
            for row, col in self.get_possible_moves(board):
                board.place_move(row, col, self.player)
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                board.undo_move(row, col)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in self.get_possible_moves(board):
                board.place_move(row, col, self.opponent)
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                board.undo_move(row, col)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_possible_moves(self, board):
        possible_moves = []
        for row in range(board.rows):
            for col in range(board.cols):
                if board.is_empty(row, col):
                    possible_moves.append((row, col))
        return possible_moves

    def evaluate_board(self, board):
        score = 0

        # Evaluate for the AI's moves (self.player)
        score += self.evaluate_player(board, self.player)

        # Evaluate for the opponent's moves (self.opponent)
        score -= self.evaluate_player(board, self.opponent)

        return score

    def evaluate_player(self, board, player):
        # Evaluate the board for a given player
        score = 0

        # Count potential rows, columns, and diagonals for the player
        for row in range(board.rows):
            for col in range(board.cols):
                if board.get_board()[row][col] == player:
                    score += self.evaluate_position(board, row, col, player)

        return score

    def evaluate_position(self, board, row, col, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # right, down, diagonal-down-right, diagonal-down-left
        score = 0

        for d_row, d_col in directions:
            score += self.evaluate_line(board, row, col, player, d_row, d_col)

        return score

    def evaluate_line(self, board, row, col, player, d_row, d_col):
        # Evaluate both directions (positive and negative) for continuity
        count, block_score = 0, 0
        r, c = row + d_row, col + d_col

        # Check continuity in one direction
        while 0 <= r < board.rows and 0 <= c < board.cols:
            if board.get_board()[r][c] == player:
                count += 1
            elif board.is_empty(r, c):
                block_score += 0.5  # Open-ended, more flexible
                break
            else:
                break  # Opponent piece, not a continuation
            r += d_row
            c += d_col

        # Evaluate the other direction
        r, c = row - d_row, col - d_col
        while 0 <= r < board.rows and 0 <= c < board.cols:
            if board.get_board()[r][c] == player:
                count += 1
            elif board.is_empty(r, c):
                block_score += 0.5  # Open-ended, more flexible
                break
            else:
                break
            r -= d_row
            c -= d_col

        # Higher score for longer lines and open-ended ones
        if count >= 4:  # Win condition
            return 100
        elif count == 3 and block_score > 0:
            return 50  # High potential for threat formation
        elif count == 2 and block_score > 0:
            return 20  # Some potential for future moves

        return count + block_score  # Sum up total score

    def count_line(self, board, row, col, player, d_row, d_col):
        count = 0
        r, c = row + d_row, col + d_col

        # Check one direction for continuity of the player's pieces
        while 0 <= r < board.rows and 0 <= c < board.cols and board.get_board()[r][c] == player:
            count += 1
            r += d_row
            c += d_col

        return count
