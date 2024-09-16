from AI.minmax import MinimaxAI


class HybridAI:
    def __init__(self, player, rules, first_player_move, rl_model, max_depth=3):
        self.minimax_ai = MinimaxAI(player, rules, first_player_move, max_depth)
        self.rl_model = rl_model

    def get_move(self, board):
        return self.minimax_ai.get_move(board)
