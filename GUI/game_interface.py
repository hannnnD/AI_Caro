import pygame
import time  # Để thêm thời gian trễ cho chế độ AI vs AI

class GameInterface:
    def __init__(self, board_size, width=1280, height=720):
        pygame.init()
        self.board_size = board_size
        self.cell_size = 50
        self.width = self.board_size * self.cell_size + 200  # Thêm khoảng trống bên trái cho các nút
        self.height = self.board_size * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board_size = board_size
        self.width = width
        self.height = height
        pygame.display.set_caption("Cờ Caro")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.colors = {
            "background": (255, 255, 255),
            "lines": (23, 145, 135),
            "player1": (242, 85, 96),
            "player2": (28, 170, 156)
        }
        self.font = pygame.font.Font(None, 26)
        # Vị trí và kích thước của các nút chọn chế độ
        self.button_pvp = pygame.Rect(10, 50, 130, 50)
        self.button_pve = pygame.Rect(10, 120, 130, 50)
        self.button_eve = pygame.Rect(10, 190, 130, 50)

    def draw_board(self, board):
        self.screen.fill(self.colors["background"])

        # Draw grid lines
        for i in range(self.board_size + 1):
            pygame.draw.line(self.screen, self.colors["lines"], (i * self.cell_size + 150, 0),
                             (i * self.cell_size + 150, self.board_size * self.cell_size))
            pygame.draw.line(self.screen, self.colors["lines"], (150, i * self.cell_size),
                             (self.width, i * self.cell_size))

        # Draw X and O pieces
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

        # Hiển thị các nút chọn chế độ bên trái của màn hình
        self.display_mode_buttons()

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Kiểm tra xem người chơi có nhấn vào khu vực bàn cờ không
                if x > 150:  # Vùng bên phải nơi bàn cờ hiển thị
                    col = (x - 150) // self.cell_size
                    row = y // self.cell_size
                    return True, (row, col)
        return True, None

    def display_mode_selection(self):
        running = True
        mode = None
        while running:
            self.screen.fill(self.colors["background"])
            self.display_mode_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.button_pvp.collidepoint(x, y):
                        return "PVP"
                    elif self.button_pve.collidepoint(x, y):
                        return "PVE"
                    elif self.button_eve.collidepoint(x, y):
                        return "EVE"
            pygame.display.flip()

    def display_mode_buttons(self):
        # Hiển thị các nút chọn chế độ bên trái của màn hình
        pygame.draw.rect(self.screen, (0, 255, 0), self.button_pvp)
        pvp_text = self.font.render("PvP", True, (0, 0, 0))
        self.screen.blit(pvp_text, (self.button_pvp.x + 5, self.button_pvp.y + 10))

        pygame.draw.rect(self.screen, (0, 255, 0), self.button_pve)
        pve_text = self.font.render("PvE", True, (0, 0, 0))
        self.screen.blit(pve_text, (self.button_pve.x + 5, self.button_pve.y + 10))

        pygame.draw.rect(self.screen, (0, 255, 0), self.button_eve)
        eve_text = self.font.render("EvE", True, (0, 0, 0))
        self.screen.blit(eve_text, (self.button_eve.x + 5, self.button_eve.y + 10))

    def show_winner(self, winner):
        text = self.font.render(f"Player {winner} wins!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2 + 75, self.board_size * self.cell_size // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def quit(self):
        pygame.quit()

    def update(self):
        pygame.display.flip()

    def delay_for_ai_vs_ai(self):
        """Thêm độ trễ cho chế độ AI vs AI"""
        time.sleep(1)
