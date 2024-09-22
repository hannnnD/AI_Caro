def check_winner(board):
  for i in range(3):
    if board[i][0] == board[i][1] == board[i][2] != 0:
      return board[i][0]

  for j in range(3):
    if board[0][j] == board[1][j] == board[2][j] != 0:
      return board[0][j]

  if board[0][0] == board[1][1] == board[2][2] != 0:
    return board[0][0]
  if board[0][2] == board[1][1] == board[2][0] != 0:
    return board[0][2]

  return 0

def is_full(board):
  for i in range(3):
    for j in range(3):
      if board[i][j] == 0:
        return False
  return True

def count_early_endings(board, player, early_endings_count):

  winner = check_winner(board)
  if winner != 0 or is_full(board):
    early_endings_count[0] += 1
    return

  for i in range(3):
    for j in range(3):
      if board[i][j] == 0:
        board[i][j] = player
        count_early_endings(board, 3 - player, early_endings_count)
        board[i][j] = 0

initial_board = [[0, 0, 0],
                 [0, 1, 0],
                 [0, 0, 0]]

early_endings_count = [0]

count_early_endings(initial_board, 2, early_endings_count)

print("Số trường hợp kết thúc sớm:", early_endings_count[0])