import hashlib
import numpy as np

class ReinforcementLearning:
    def __init__(self):
        self.model = {}

    def train(self, game_records):
        for record in game_records:
            board_state, move, result = record
            # Cập nhật mô hình với các phần thưởng chi tiết hơn
            for variant in self.get_board_variants(board_state):
                board_hash = self.hash_board(variant)
                if board_hash not in self.model:
                    self.model[board_hash] = {}
                if move not in self.model[board_hash]:
                    self.model[board_hash][move] = 0
                self.model[board_hash][move] += result

    def update(self, board_state, move, reward):
        board_hash = self.hash_board(board_state)
        if board_hash not in self.model:
            self.model[board_hash] = {}
        if move not in self.model[board_hash]:
            self.model[board_hash][move] = 0
        self.model[board_hash][move] += reward

    def predict_move(self, board, player):
        board_hash = self.hash_board(board)
        if board_hash in self.model:
            # Chọn nước đi tốt nhất dựa trên phần thưởng cao nhất
            return max(self.model[board_hash], key=self.model[board_hash].get)
        return None

    def get_board_variants(self, board_state):
        """
        Tạo ra các biến thể của bàn cờ (các trạng thái xoay và đối xứng)
        """
        variants = []
        board_np = np.array(board_state)

        # Thêm biến thể gốc
        variants.append(board_np)

        # Các biến thể sau khi xoay
        for i in range(1, 4):
            board_np = np.rot90(board_np)
            variants.append(board_np)

        # Các biến thể đối xứng
        flipped = np.fliplr(board_np)
        variants.append(flipped)
        for i in range(1, 4):
            flipped = np.rot90(flipped)
            variants.append(flipped)

        return variants

    def hash_board(self, board_state):
        # Normalize the board before hashing it
        return self.normalize_board(board_state)

    def normalize_board(self, board_state):
        # Example of transforming the board by rotating or flipping it
        transformations = [
            board_state,  # Original
            np.rot90(board_state),  # 90 degrees rotation
            np.rot90(board_state, 2),  # 180 degrees rotation
            np.rot90(board_state, 3),  # 270 degrees rotation
            np.fliplr(board_state),  # Flip horizontally
            np.fliplr(np.rot90(board_state)),  # Flip horizontally and rotate 90 degrees
            np.fliplr(np.rot90(board_state, 2)),  # Flip horizontally and rotate 180 degrees
            np.fliplr(np.rot90(board_state, 3))  # Flip horizontally and rotate 270 degrees
        ]

        # Choose the transformation that produces the smallest hash value
        return min(hashlib.sha256(str(t).encode()).hexdigest() for t in transformations)
