def check_winner(board):
  """Kiểm tra xem có người chiến thắng hay không.

  Args:
      board: Bàn cờ hiện tại.

  Returns:
      1 nếu X thắng, 2 nếu O thắng, 0 nếu chưa có ai thắng.
  """

  # Kiểm tra các hàng
  for i in range(3):
    if board[i][0] == board[i][1] == board[i][2] != 0:
      return board[i][0]

  # Kiểm tra các cột
  for j in range(3):
    if board[0][j] == board[1][j] == board[2][j] != 0:
      return board[0][j]

  # Kiểm tra các đường chéo
  if board[0][0] == board[1][1] == board[2][2] != 0:
    return board[0][0]
  if board[0][2] == board[1][1] == board[2][0] != 0:
    return board[0][2]

  return 0  # Chưa có ai thắng

def is_full(board):
  """Kiểm tra xem bàn cờ đã đầy hay chưa.

  Args:
      board: Bàn cờ hiện tại.

  Returns:
      True nếu bàn cờ đã đầy, False nếu chưa.
  """

  for i in range(3):
    for j in range(3):
      if board[i][j] == 0:
        return False
  return True

def count_early_endings(board, player, early_endings_count):
  """Đếm số trường hợp kết thúc sớm.

  Args:
      board: Bàn cờ hiện tại.
      player: Người chơi hiện tại (1 hoặc 2).
      early_endings_count: Biến đếm số trường hợp kết thúc sớm.
  """

  winner = check_winner(board)
  if winner != 0 or is_full(board):
    # Kết thúc sớm (có người thắng hoặc hòa)
    early_endings_count[0] += 1
    return

  for i in range(3):
    for j in range(3):
      if board[i][j] == 0:
        board[i][j] = player
        count_early_endings(board, 3 - player, early_endings_count)  # Đổi người chơi
        board[i][j] = 0  # Hoàn tác nước đi

# Khởi tạo bàn cờ với X đã đánh vào ô (0, 0)
initial_board = [[0, 0, 0],
                 [0, 1, 0],
                 [0, 0, 0]]

# Biến đếm số trường hợp kết thúc sớm
early_endings_count = [0]

# Bắt đầu đếm từ lượt của O
count_early_endings(initial_board, 2, early_endings_count)

# In kết quả
print("Số trường hợp kết thúc sớm:", early_endings_count[0])