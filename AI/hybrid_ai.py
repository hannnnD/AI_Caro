from AI.minmax import MinimaxAI
from AI.reinforcement_learning import ReinforcementLearning

class HybridAI:
    def __init__(self, player, rules, first_player_move, rl_model, max_depth=3):
        self.minimax_ai = MinimaxAI(player, rules, first_player_move, max_depth)
        self.rl_model = rl_model

    def get_move(self, board):
        # Check if the RL model has a learned move
        rl_move = self.rl_model.get_move(board)
        if rl_move:
            print(f"RL move found: {rl_move}")
            return rl_move

        # If no RL move is found, fall back to Minimax
        print("No RL move found, falling back to Minimax")
        return self.minimax_ai.get_move(board)
