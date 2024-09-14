import hashlib

class ReinforcementLearning:
    def __init__(self):
        self.model = {}

    def train(self, game_records):
        for record in game_records:
            board_state, move, result = record
            board_hash = self.hash_board(board_state)
            self.model[board_hash] = move

    def get_move(self, board):
        board_hash = self.hash_board(board.get_board())
        if board_hash in self.model:
            return self.model[board_hash]
        return None

    def hash_board(self, board_state):
        return hashlib.sha256(str(board_state).encode()).hexdigest()
