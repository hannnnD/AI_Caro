import json

class TrainingData:
    def __init__(self):
        self.records = []

    def add_record(self, board_state, move, player, result=None):
        # Add the result of the game (win/lose/draw) to the record
        self.records.append({"board": board_state, "move": move, "player": player, "result": result})

    def save_to_file(self, filename):
        with open(filename, 'a') as file:
            json.dump(self.records, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.records = json.load(file)
        except FileNotFoundError:
            print("No past data available.")

    def get_past_moves(self, current_board, player):
        possible_moves = []
        for record in self.records:
            if record["board"] == current_board and record["player"] == player:
                possible_moves.append(record["move"])
        return possible_moves
