from AI_2.competitive_ai import CompetitiveAI
from AI.hybrid_ai import HybridAI
from AI_2.reinforcement_learning import ReinforcementLearning
from Data.training_data import TrainingData
from GUI.game_interface import GameInterface
from Game.board import Board
from Game.rules import Rules
import pygame


def main():
    pygame.init()
    game_interface = GameInterface(board_size=15)

    game_mode = game_interface.display_mode_selection()

    if game_mode == "PVP":
        player_vs_player(game_interface)
    elif game_mode == "PVE":
        player_vs_ai(game_interface)
    elif game_mode == "EVE":
        ai_vs_ai_competition(game_interface)


def player_vs_player(game_interface):
    board = Board(15, 15)
    rules = Rules()
    training_data = TrainingData()

    running = True
    current_player = 1

    while running:
        game_interface.draw_board(board.get_board())
        running, move = game_interface.handle_events()

        if move:
            row, col = move
            if board.is_empty(row, col):
                board.place_move(row, col, current_player)
                training_data.add_record(board.get_board(), (row, col), current_player)

                if rules.check_winner(board, row, col, current_player):
                    game_interface.show_winner(current_player)
                    running = False
                current_player = 3 - current_player

    training_data.save_to_file("game_records.txt")

    game_interface.quit()


def player_vs_ai(game_interface):
    board = Board(15, 15)
    rules = Rules()
    training_data = TrainingData()  # Initialize the training data recorder

    first_player_move = None
    rl_model = train_ai_from_past_games()  # Load and train the RL model
    ai = HybridAI(2, rules, first_player_move, rl_model)  # Use Hybrid AI (Minimax + RL)

    running = True
    current_player = 2  # AI starts first

    while running:
        game_interface.draw_board(board.get_board())
        running, move = game_interface.handle_events()

        if current_player == 1 and move:
            row, col = move
            if first_player_move is None:
                first_player_move = (row, col)
                ai.minimax_ai.first_player_move = first_player_move

            if board.is_empty(row, col):
                board.place_move(row, col, current_player)
                ai.minimax_ai.player_moves.append((row, col))
                training_data.add_record(board.get_board(), (row, col), current_player)  # Record move
                if rules.check_winner(board, row, col, current_player):
                    game_interface.show_winner(current_player)
                    running = False
                current_player = 2

        elif current_player == 2:
            if len(ai.minimax_ai.ai_moves) == 0:  # Check if AI is making the first move
                move = ai.minimax_ai.get_first_move(board)  # Get the first move
            else:
                move = ai.get_move(board)  # Regular move for subsequent turns

            if move is not None:
                row, col = move
                board.place_move(row, col, current_player)
                ai.minimax_ai.ai_moves.append((row, col))
                training_data.add_record(board.get_board(), (row, col), current_player)  # Record AI move
                if rules.check_winner(board, row, col, current_player):
                    game_interface.show_winner(current_player)
                    running = False
                current_player = 1
            else:
                print("AI could not find a valid move.")
                running = False


    game_interface.quit()


def ai_vs_ai_competition(game_interface):
    board = Board(15, 15)
    rules = Rules()

    # AI hiện tại (HybridAI)
    rl_model_existing = train_ai_from_past_games()
    ai_existing = HybridAI(1, rules, None, rl_model_existing)

    # AI mới (CompetitiveAI)
    ai_new = CompetitiveAI(2, rules)

    running = True
    current_player = 1

    while running:
        game_interface.draw_board(board.get_board())

        if current_player == 1:
            move = ai_existing.get_move(board)
        else:
            move = ai_new.get_move(board)

        if move:
            row, col = move
            board.place_move(row, col, current_player)

            if rules.check_winner(board, row, col, current_player):
                game_interface.show_winner(current_player)
                running = False

            current_player = 3 - current_player

    game_interface.quit()



def train_ai_from_past_games():
    training_data = TrainingData()
    training_data.load_from_file("game_records.txt")
    rl_model = ReinforcementLearning()
    rl_model.train(training_data.get_records())
    return rl_model


if __name__ == "__main__":
    main()
