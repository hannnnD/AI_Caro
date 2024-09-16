import random
from AI_2.reinforcement_learning import ReinforcementLearning
from Data.training_data import TrainingData

class CompetitiveAI:
    def __init__(self, player, rules):
        self.player = player
        self.rules = rules
        self.rl_model = ReinforcementLearning()  # Sử dụng mô hình RL cho AI mới
        self.move_history = []  # Lưu lại lịch sử các nước đi

    def get_move(self, board):
        # AI sử dụng mô hình RL để dự đoán nước đi tốt nhất dựa trên trạng thái bàn cờ
        move = self.rl_model.predict_move(board.get_board(), self.player)
        if move is not None:
            print(f"Competitive AI Move Chosen: {move}")
            return move
        else:
            # Nếu không tìm được nước đi, chọn nước ngẫu nhiên
            possible_moves = self.get_possible_moves(board)
            if possible_moves:
                move = random.choice(possible_moves)
                return move
            else:
                return None

    def get_possible_moves(self, board):
        # Lấy danh sách các vị trí trống trên bàn cờ
        possible_moves = []
        for row in range(board.rows):
            for col in range(board.cols):
                if board.is_empty(row, col):
                    possible_moves.append((row, col))
        return possible_moves

    def learn_from_game(self, board, move_history):
        """
        Học từ ván đấu đã kết thúc để cải thiện khả năng chơi.
        """
        winner = self.rules.is_game_over(board, self.player)
        reward = 1 if winner == self.player else -1

        # Cập nhật mô hình RL với từng trạng thái bàn cờ và nước đi trong lịch sử ván
        for board_state, move in move_history:
            self.rl_model.update(board_state, move, reward)

    def train_from_past_games(self, filename):
        # Tải và huấn luyện từ dữ liệu các ván chơi trước
        training_data = TrainingData()
        training_data.load_from_file(filename)
        self.rl_model.train(training_data.get_records())

    def save_training_data(self, filename, move_history):
        # Lưu dữ liệu ván đấu vào file để tiếp tục huấn luyện
        training_data = TrainingData()
        training_data.add_records(move_history)
        training_data.save_to_file(filename)
