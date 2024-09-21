class TrainingData:
    def __init__(self):
        self.data = []  # assuming training data is stored in a list

    def add_record(self, board, move, player):
        self.data.append((board, move, player))

    def clear(self):
        self.data.clear()  # Clear the stored training data


