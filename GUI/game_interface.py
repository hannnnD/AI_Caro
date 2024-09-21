import pygame
import time

class GameInterface:
    def __init__(self, board_size, width=1280, height=720):
        pygame.init()
        self.board_size = board_size
        self.cell_size = 50
        self.width = self.board_size * self.cell_size + 200  # Thêm khoảng trống bên trái cho các nút
        self.height = self.board_size * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.colors = {
            "background": (250, 250, 250),
            "lines": (23, 145, 135),
            "player1": (242, 85, 96),
            "player2": (28, 170, 156)
        }
        self.font = pygame.font.Font(None, 26)
        # Vị trí và kích thước của các nút
        self.button_reset = pygame.Rect(10, 50, 130, 50)
        self.button_undo = pygame.Rect(10, 120, 130, 50)

    def draw_board(self, board):
        self.screen.fill(self.colors["background"])

        # Vẽ các đường kẻ
        for i in range(self.board_size + 1):
            pygame.draw.line(self.screen, self.colors["lines"], (i * self.cell_size + 150, 0),
                             (i * self.cell_size + 150, self.board_size * self.cell_size))
            pygame.draw.line(self.screen, self.colors["lines"], (150, i * self.cell_size),
                             (self.width, i * self.cell_size))

        # Vẽ các quân cờ X và O
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == 1:  # Player 1 (X)
                    start_pos1 = (col * self.cell_size + 155, row * self.cell_size + 5)
                    end_pos1 = (col * self.cell_size + self.cell_size + 145, row * self.cell_size + self.cell_size - 5)
                    pygame.draw.line(self.screen, self.colors["player1"], start_pos1, end_pos1, 5)

                    start_pos2 = (col * self.cell_size + 155, row * self.cell_size + self.cell_size - 5)
                    end_pos2 = (col * self.cell_size + self.cell_size + 145, row * self.cell_size + 5)
                    pygame.draw.line(self.screen, self.colors["player1"], start_pos2, end_pos2, 5)

                elif board[row][col] == 2:  # Player 2 (O)
                    pygame.draw.circle(self.screen, self.colors["player2"],
                                       (col * self.cell_size + self.cell_size // 2 + 150,
                                        row * self.cell_size + self.cell_size // 2),
                                       self.cell_size // 2 - 5, 5)

        self.display_buttons()
        pygame.display.flip()

    def check_four_in_a_row(self, board, row, col, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for d_row, d_col in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i * d_row, col + i * d_col
                if 0 <= r < self.board_size and 0 <= c < self.board_size and board[r][c] == player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - i * d_row, col - i * d_col
                if 0 <= r < self.board_size and 0 <= c < self.board_size and board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def display_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Button colors for different states
        reset_color = (28, 170, 156)  # Default reset button color
        undo_color = (242, 85, 96)  # Default undo button color

        # Change color on hover for the reset button
        if self.button_reset.collidepoint(mouse_pos):
            reset_color = (28, 170, 156)  # Darker green on hover
            if mouse_click[0]:  # Mouse is clicked on the reset button
                reset_color = (28, 190, 156)  # Even darker on click

        # Change color on hover for the undo button
        if self.button_undo.collidepoint(mouse_pos):
            undo_color = (242, 85, 96)  # Darker red on hover
            if mouse_click[0]:  # Mouse is clicked on the undo button
                undo_color = (222, 85, 96)  # Even darker on click

        # Draw reset button
        pygame.draw.rect(self.screen, reset_color, self.button_reset)
        reset_text = self.font.render("Reset Game", True, (0, 0, 0))
        self.screen.blit(reset_text, (self.button_reset.x + 5, self.button_reset.y + 10))

        # Draw undo button
        pygame.draw.rect(self.screen, undo_color, self.button_undo)
        undo_text = self.font.render("Undo Move", True, (0, 0, 0))
        self.screen.blit(undo_text, (self.button_undo.x + 5, self.button_undo.y + 10))

    def show_winner(self, winner):
        text = self.font.render(f"Player {winner} wins!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2 + 75, self.board_size * self.cell_size // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def quit(self):
        pygame.quit()

    def update_display(self):
        pygame.display.flip()

    def show_message(self, message):
        text = self.font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2 + 75, self.board_size * self.cell_size // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(3)

    def get_move_from_click(self, mouse_pos, board):
        x, y = mouse_pos
        if x > 150 and x < self.width and y > 0 and y < self.height:
            col = (x - 150) // self.cell_size
            row = y // self.cell_size
            if board.is_empty(row, col):
                return row, col
        return None
