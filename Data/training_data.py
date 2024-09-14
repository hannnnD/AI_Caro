class TrainingData:
    def __init__(self):
        self.records = []

    def add_record(self, board_state, move, result):
        self.records.append((board_state.copy(), move, result))

    def get_records(self):
        return self.records

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for record in self.records:
                file.write(f"{record}\n")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    self.records.append(eval(line.strip()))
        except FileNotFoundError:
            print(f"{filename} not found. Starting with empty training data.")
