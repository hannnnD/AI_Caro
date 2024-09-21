from AI.minmax import MinimaxAI

class HybridAI:
    def __init__(self, player, rules, first_player_move, rl_model, max_depth=3):
        self.player = player
        self.rules = rules
        self.first_player_move = first_player_move
        self.rl_model = rl_model
        self.max_depth = max_depth
        self.minimax_ai = MinimaxAI(player, rules, first_player_move, max_depth)
        self.move_history = []  # Lưu trữ lịch sử các nước đi của AI

    def get_move(self, board):
        move = self.minimax_ai.get_move(board)
        if move:
            self.move_history.append(move)  # This must be called to track AI's move
        return move

    def undo_move(self):
        # Xóa nước đi cuối cùng của AI và trả lại tọa độ nước đi đã bị undo
        if self.move_history:
            last_move = self.move_history.pop()
            return last_move
        return None

    def reset(self):
        # Đặt lại lịch sử và trạng thái của AI
        self.minimax_ai = MinimaxAI(self.player, self.rules, self.first_player_move, self.max_depth)
        self.move_history.clear()
