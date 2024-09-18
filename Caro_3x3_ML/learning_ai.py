import random


class LearningAI:
    def __init__(self, player, rules, training_data):
        self.player = player
        self.rules = rules
        self.training_data = training_data

    def get_move(self, board):
        # Lấy các nước đi dẫn đến thắng trong các trò chơi trước
        winning_moves = self.get_weighted_moves(board, "win")
        if winning_moves:
            return random.choice(winning_moves)

        # Nếu không có nước đi thắng, lấy các nước đi từ dữ liệu trước hoặc chọn ngẫu nhiên
        past_moves = self.training_data.get_past_moves(board.get_board(), self.player)
        if past_moves:
            return random.choice(past_moves)

        return self.random_move(board)

    def get_weighted_moves(self, board, outcome):
        weighted_moves = []
        for record in self.training_data.records:
            if record["board"] == board.get_board() and record["result"] == outcome:
                weighted_moves.append(record["move"])
        return weighted_moves

    def random_move(self, board):
        empty_cells = [(row, col) for row in range(board.rows) for col in range(board.cols) if board.is_empty(row, col)]
        return random.choice(empty_cells) if empty_cells else None

    def get_past_moves(self, current_board, player):
        possible_moves = []
        for record in self.records:
            board_state, move, recorded_player, result = record
            # Kiểm tra xem đây có phải là lượt đi của người chơi hiện tại không (AI)
            if board_state == current_board and recorded_player == player:
                possible_moves.append(move)
        return possible_moves
