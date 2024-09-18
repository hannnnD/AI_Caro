import numpy as np
import random
import pygame
import sys

# Constants
BOARD_SIZE = 3
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1
CELL_SIZE = 200
LINE_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SCREEN_SIZE = BOARD_SIZE * CELL_SIZE
EPSILON = 0.1
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01
ALPHA = 0.2  # Learning rate for Q-learning
GAMMA = 0.9  # Discount factor for Q-learning

# Colors
WHITE = (255, 255, 255)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (28, 170, 156)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Tic-Tac-Toe')

# Initialize font
font = pygame.font.Font(None, 74)

# Draw the game grid
def draw_grid():
    screen.fill(WHITE)
    for x in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, x * CELL_SIZE), (SCREEN_SIZE, x * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_SIZE), LINE_WIDTH)

# Draw the X or O marks on the board
def draw_marks(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == PLAYER_X:
                draw_cross(row, col)
            elif board[row][col] == PLAYER_O:
                draw_circle(row, col)

# Draw X mark
def draw_cross(row, col):
    start_desc = (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4)
    end_desc = (col * CELL_SIZE + 3 * CELL_SIZE // 4, row * CELL_SIZE + 3 * CELL_SIZE // 4)
    start_asc = (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + 3 * CELL_SIZE // 4)
    end_asc = (col * CELL_SIZE + 3 * CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4)
    pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

# Draw O mark
def draw_circle(row, col):
    pygame.draw.circle(screen, CIRCLE_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

# Get row and column from mouse click position
def get_click_pos(pos):
    return pos[1] // CELL_SIZE, pos[0] // CELL_SIZE

def initialize_board():
    return np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# Check for winner
def check_winner(board):
    for i in range(BOARD_SIZE):
        # Check rows and columns
        if abs(np.sum(board[i, :])) == BOARD_SIZE:
            return np.sign(np.sum(board[i, :]))
        if abs(np.sum(board[:, i])) == BOARD_SIZE:
            return np.sign(np.sum(board[:, i]))
    # Check diagonals
    diag1 = np.sum([board[i, i] for i in range(BOARD_SIZE)])
    diag2 = np.sum([board[i, BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)])
    if abs(diag1) == BOARD_SIZE:
        return np.sign(diag1)
    if abs(diag2) == BOARD_SIZE:
        return np.sign(diag2)
    # Check for draw
    if not np.any(board == EMPTY):
        return 0
    return None

# Get possible actions (empty positions)
def get_available_actions(board):
    return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i, j] == EMPTY]

# Take an action
def take_action(board, action, player):
    board[action] = player
    return board

# Q-learning update function
def q_update(q_table, state, action, reward, next_state, done):
    state_key = tuple(state.flatten())
    next_state_key = tuple(next_state.flatten())
    if state_key not in q_table:
        q_table[state_key] = {a: 0 for a in get_available_actions(state)}
    if next_state_key not in q_table:
        q_table[next_state_key] = {a: 0 for a in get_available_actions(next_state)}
    max_next_q = max(q_table[next_state_key].values(), default=0)
    if done:
        q_table[state_key][action] = reward
    else:
        q_table[state_key][action] += ALPHA * (reward + GAMMA * max_next_q - q_table[state_key][action])

# AI chọn hành động
def choose_action(q_table, state, available_actions, epsilon):
    state_key = tuple(state.flatten())
    if random.uniform(0, 1) < epsilon:
        return random.choice(available_actions)  # Exploration
    if state_key in q_table:
        q_values = q_table[state_key]
        return max(q_values, key=q_values.get)
    return random.choice(available_actions)

# Train AI
def train_q_learning(episodes=5000, epsilon=EPSILON, epsilon_decay=EPSILON_DECAY, min_epsilon=MIN_EPSILON):
    q_table = {}
    for episode in range(episodes):
        state = initialize_board()
        done = False
        player = PLAYER_X
        while not done:
            available_actions = get_available_actions(state)
            action = choose_action(q_table, state, available_actions, epsilon)
            next_state = take_action(state.copy(), action, player)
            winner = check_winner(next_state)
            reward = 1 if winner == player else 0.7 if winner == 0 else -1
            done = winner is not None
            q_update(q_table, state, action, reward, next_state, done)
            state = next_state
            player = PLAYER_O if player == PLAYER_X else PLAYER_X
        epsilon = max(min_epsilon, epsilon * epsilon_decay)
    return q_table

# Play game
def play_game(q_table):
    board = initialize_board()
    done = False
    player = PLAYER_X
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and player == PLAYER_X:
                row, col = get_click_pos(pygame.mouse.get_pos())
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    winner = check_winner(board)
                    done = winner is not None
                    player = PLAYER_O
        if player == PLAYER_O and not done:
            available_actions = get_available_actions(board)
            state_key = tuple(board.flatten())
            action = max(q_table.get(state_key, {}), key=q_table[state_key].get, default=random.choice(available_actions))
            board[action[0], action[1]] = PLAYER_O
            winner = check_winner(board)
            done = winner is not None
            player = PLAYER_X
        draw_grid()
        draw_marks(board)
        pygame.display.update()

# Train AI and play the game
q_table = train_q_learning()
play_game(q_table)
