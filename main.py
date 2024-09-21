import pygame

from AI.hybrid_ai import HybridAI
from Data.training_data import TrainingData
from GUI.game_interface import GameInterface
from Game.board import Board
from Game.rules import Rules


def main():
    pygame.init()
    game_interface = GameInterface(board_size=15)

    # Directly start Player vs AI mode
    player_vs_ai(game_interface)

    game_interface.quit()


def player_vs_ai(game_interface):
    board_size = 15
    board = Board(board_size, board_size)
    rules = Rules()
    training_data = TrainingData()  # Initialize the training data recorder

    # Ensure AI makes the first move in the center
    first_player_move = (board_size // 2, board_size // 2)

    rl_model = train_ai_from_past_games()  # Load and train the RL model
    ai = HybridAI(2, rules, first_player_move, rl_model)  # Hybrid AI (Minimax + RL)

    current_player = 2  # Human player starts first
    move_history = []  # To store the history of moves for Undo functionality

    running = True

    while running:
        game_running = True
        winner = None

        while game_running:
            game_interface.draw_board(board.get_board())
            game_interface.display_buttons()  # Draw "Restart" and "Undo" buttons
            game_interface.update_display()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if game_interface.button_reset.collidepoint(mouse_pos):
                        handle_restart(board, ai, move_history, training_data)
                        break
                    elif game_interface.button_undo.collidepoint(mouse_pos):
                        handle_undo(board, ai, move_history, current_player, game_interface)
                        #current_player = switch_player(current_player)

                    else:
                        if current_player == 1:
                            move = game_interface.get_move_from_click(mouse_pos, board)
                            if move and board.is_empty(*move):
                                execute_player_move(move, board, move_history, training_data, current_player)
                                if rules.check_winner(board, *move, current_player):
                                    winner = current_player
                                    game_running = False
                                current_player = 2

            # AI's turn
            if game_running and current_player == 2:
                if not move_history:  # AI's first move in the center
                    move = first_player_move
                else:
                    move = ai.get_move(board)
                if move:
                    execute_player_move(move, board, move_history, training_data, current_player)
                    if rules.check_winner(board, *move, current_player):
                        winner = current_player
                        game_running = False
                    current_player = 1

        # Handle end of game
        handle_end_of_game(game_interface, winner, training_data, board, ai, move_history)


def train_ai_from_past_games():
    pass


def handle_restart(board, ai, move_history, training_data):
    board.reset()
    ai.reset()
    move_history.clear()
    training_data.clear()


def handle_undo(board, ai, move_history, current_player, game_interface):
    if move_history:
        last_move = move_history.pop()
        print(f"Undoing player's move: {last_move}")
        board.undo_move(*last_move)

        # Cập nhật giao diện sau khi undo
        game_interface.draw_board(board.get_board())
        game_interface.update_display()

        if current_player == 2:  # AI's turn was last
            ai_last_move = ai.undo_move()
            if ai_last_move:
                print(f"Undoing AI's move: {ai_last_move}")
                board.undo_move(*ai_last_move)

                # Cập nhật giao diện sau khi undo nước của AI
                game_interface.draw_board(board.get_board())
                game_interface.update_display()

                # Sau khi AI undo, không cần chuyển ngay về người chơi mà chỉ cần đợi
                current_player = 1  # Switch back to player

        else:
            current_player = switch_player(current_player)

    # Sau khi hoàn tất undo, cập nhật lại giao diện để hiển thị thay đổi
    game_interface.draw_board(board.get_board())
    game_interface.update_display()

def switch_player(current_player):
    return 1 if current_player == 2 else 2


def execute_player_move(move, board, move_history, training_data, current_player):
    board.place_move(*move, current_player)
    move_history.append(move)
    print(f"Move added to history: {move}")  # Debugging
    training_data.add_record(board.get_board(), move, current_player)



def handle_end_of_game(game_interface, winner, training_data, board, ai, move_history):
    if winner:
        game_interface.show_winner(winner)
    else:
        game_interface.show_message("Game Over")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if game_interface.button_reset.collidepoint(mouse_pos):
                    handle_restart(board, ai, move_history, training_data)
                    return
        game_interface.draw_board(board.get_board())
        game_interface.display_buttons()
        game_interface.update_display()


if __name__ == "__main__":
    main()
