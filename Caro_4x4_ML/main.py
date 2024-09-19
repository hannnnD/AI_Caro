import random
from copy import deepcopy

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3
BOARD_FORMAT = (
    "-----------------------------------------------------------------\n"
    "| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} |\n"
    "|----------------------------------------------------------------|\n"
    "| {10} | {11} | {12} | {13} | {14} | {15} | {16} | {17} | {18} | {19} |\n"
    "|----------------------------------------------------------------|\n"
    "| {20} | {21} | {22} | {23} | {24} | {25} | {26} | {27} | {28} | {29} |\n"
    "|----------------------------------------------------------------|\n"
    "| {30} | {31} | {32} | {33} | {34} | {35} | {36} | {37} | {38} | {39} |\n"
    "|----------------------------------------------------------------|\n"
    "| {40} | {41} | {42} | {43} | {44} | {45} | {46} | {47} | {48} | {49} |\n"
    "|----------------------------------------------------------------|\n"
    "| {50} | {51} | {52} | {53} | {54} | {55} | {56} | {57} | {58} | {59} |\n"
    "|----------------------------------------------------------------|\n"
    "| {60} | {61} | {62} | {63} | {64} | {65} | {66} | {67} | {68} | {69} |\n"
    "|----------------------------------------------------------------|\n"
    "| {70} | {71} | {72} | {73} | {74} | {75} | {76} | {77} | {78} | {79} |\n"
    "|----------------------------------------------------------------|\n"
    "| {80} | {81} | {82} | {83} | {84} | {85} | {86} | {87} | {88} | {89} |\n"
    "|----------------------------------------------------------------|\n"
    "| {90} | {91} | {92} | {93} | {94} | {95} | {96} | {97} | {98} | {99} |\n"
    "-----------------------------------------------------------------"
)

BOARD_SIZE = 10  # Kích thước bàn cờ
WIN_COUNT = 4
NAMES = [' ', 'X', 'O']

def printboard(state):
    for row in state:
        print(" | ".join(NAMES[cell].center(2) for cell in row))
        print('-' * (BOARD_SIZE * 4 - 1))

def emptystate():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def gameover(state):
    # Kiểm tra hàng ngang, dọc và đường chéo
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if state[i][j] != EMPTY:
                # Kiểm tra theo hàng
                if j <= BOARD_SIZE - WIN_COUNT and all(state[i][j + k] == state[i][j] for k in range(WIN_COUNT)):
                    return state[i][j]
                # Kiểm tra theo cột
                if i <= BOARD_SIZE - WIN_COUNT and all(state[i + k][j] == state[i][j] for k in range(WIN_COUNT)):
                    return state[i][j]
                # Kiểm tra đường chéo chính
                if i <= BOARD_SIZE - WIN_COUNT and j <= BOARD_SIZE - WIN_COUNT and all(state[i + k][j + k] == state[i][j] for k in range(WIN_COUNT)):
                    return state[i][j]
                # Kiểm tra đường chéo phụ
                if i <= BOARD_SIZE - WIN_COUNT and j >= WIN_COUNT - 1 and all(state[i + k][j - k] == state[i][j] for k in range(WIN_COUNT)):
                    return state[i][j]

    # Kiểm tra nếu còn ô trống
    for row in state:
        if EMPTY in row:
            return EMPTY
    return DRAW

def last_to_act(state):
    countx = 0
    counto = 0
    for row in state:
        countx += row.count(PLAYER_X)
        counto += row.count(PLAYER_O)
    if countx == counto:
        return PLAYER_O
    if countx == (counto + 1):
        return PLAYER_X
    return -1


def enumstates(state, idx, agent):
    if idx >= BOARD_SIZE * BOARD_SIZE:
        player = last_to_act(state)
        if player == agent.player:
            agent.add(state)
    else:
        winner = gameover(state)
        if winner != EMPTY:
            return
        i = int(idx / BOARD_SIZE)
        j = int(idx % BOARD_SIZE)
        for val in range(3):
            state[i][j] = val
            enumstates(state, idx + 1, agent)


class Agent(object):
    def __init__(self, player, verbose=False, lossval=0, learning=True):
        self.values = {}
        self.player = player
        self.verbose = verbose
        self.lossval = lossval
        self.learning = learning
        self.epsilon = 0.1
        self.alpha = 0.99
        self.prevstate = None
        self.prevscore = 0
        self.count = 0
        self.center_moves = [(4, 4), (4, 5), (5, 4), (5, 5)]  # Vị trí 4 ô trung tâm
        enumstates(emptystate(), 0, self)

    def episode_over(self, winner):
        self.backup(self.winnerval(winner))
        self.prevstate = None
        self.prevscore = 0

    def action(self, state):
        # Ưu tiên đánh vào các ô trung tâm nếu có thể
        for move in self.center_moves:
            if state[move[0]][move[1]] == EMPTY:
                self.log(f'>>>>>>> Prioritized action to center: {move}')
                return move

        # Giảm độ sâu xuống còn 3
        _, move = self.minimax(state, depth=3, alpha=-float('inf'), beta=float('inf'),
                               maximizingPlayer=(self.player == PLAYER_X))
        self.log('>>>>>>> Best action: ' + str(move))
        return move

    def minimax(self, state, depth, alpha, beta, maximizingPlayer):
        # Kiểm tra nếu trò chơi đã kết thúc
        winner = gameover(state)
        if winner != EMPTY:
            return self.winnerval(winner), None  # Sử dụng winnerval cho trạng thái kết thúc

        # Nếu hết độ sâu
        if depth == 0:
            return self.evaluate_state(state), None  # Sử dụng evaluate_state cho trạng thái chưa kết thúc

        if maximizingPlayer:
            maxEval = -float('inf')
            bestMove = None
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if state[i][j] == EMPTY:
                        state[i][j] = PLAYER_X
                        eval, _ = self.minimax(state, depth - 1, alpha, beta, False)
                        state[i][j] = EMPTY
                        if eval > maxEval:
                            maxEval = eval
                            bestMove = (i, j)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if state[i][j] == EMPTY:
                        state[i][j] = PLAYER_O
                        eval, _ = self.minimax(state, depth - 1, alpha, beta, True)
                        state[i][j] = EMPTY
                        if eval < minEval:
                            minEval = eval
                            bestMove = (i, j)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return minEval, bestMove

    # Hàm winnerval để trả về giá trị khi trò chơi đã kết thúc
    def winnerval(self, winner):
        if winner == self.player:
            return 1
        elif winner == EMPTY:
            return 0.5
        elif winner == DRAW:
            return 0
        else:
            return self.lossval

    # Hàm evaluate_state để đánh giá trạng thái chưa kết thúc
    def evaluate_state(self, state):
        score = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if state[i][j] == self.player:
                    score += 1
                elif state[i][j] != EMPTY:
                    score -= 1
        return score

    def backup(self, nextval):
        if self.prevstate is not None and self.learning:
            self.values[self.prevstate] += self.alpha * (nextval - self.prevscore)

    def lookup(self, state):
        key = self.statetuple(state)
        if key not in self.values:
            self.add(key)
        return self.values[key]

    def add(self, state):
        winner = gameover(state)
        tup = self.statetuple(state)
        self.values[tup] = self.winnerval(winner)

    def statetuple(self, state):
        return tuple(tuple(row) for row in state)

    def log(self, s):
        if self.verbose:
            print(s)


class Human(object):
    def __init__(self, player):
        self.player = player

    def action(self, state):
        printboard(state)
        action = input('Your move? i.e. x,y : ')
        return (int(action.split(',')[0]),int(action.split(',')[1]))

    def episode_over(self, winner):
        if winner == DRAW:
            print('Game over! It was a draw.')
        else:
            print('Game over! Winner: Player {0}'.format(winner))

def play(agent1, agent2):
    state = emptystate()
    for i in range(100):  # 100 lần thay vì 9
        if i % 2 == 0:
            move = agent1.action(state)
        else:
            move = agent2.action(state)
        state[move[0]][move[1]] = (i % 2) + 1
        winner = gameover(state)
        if winner != EMPTY:
            return winner
    return winner


def measure_performance_vs_random(agent1, agent2):
    epsilon1 = agent1.epsilon
    epsilon2 = agent2.epsilon
    agent1.epsilon = 0
    agent2.epsilon = 0
    agent1.learning = False
    agent2.learning = False
    r1 = Agent(1)
    r2 = Agent(2)
    r1.epsilon = 1
    r2.epsilon = 1
    probs = [0,0,0,0,0,0]
    games = 100
    for i in range(games):
        winner = play(agent1, r2)
        if winner == PLAYER_X:
            probs[0] += 1.0 / games
        elif winner == PLAYER_O:
            probs[1] += 1.0 / games
        else:
            probs[2] += 1.0 / games
    for i in range(games):
        winner = play(r1, agent2)
        if winner == PLAYER_O:
            probs[3] += 1.0 / games
        elif winner == PLAYER_X:
            probs[4] += 1.0 / games
        else:
            probs[5] += 1.0 / games
    agent1.epsilon = epsilon1
    agent2.epsilon = epsilon2
    agent1.learning = True
    agent2.learning = True
    return probs

def measure_performance_vs_each_other(agent1, agent2):
    probs = [0,0,0]
    games = 100
    for i in range(games):
        winner = play(agent1, agent2)
        if winner == PLAYER_X:
            probs[0] += 1.0 / games
        elif winner == PLAYER_O:
            probs[1] += 1.0 / games
        else:
            probs[2] += 1.0 / games
    return probs


if __name__ == "__main__":
    p1 = Agent(1, lossval = -1)
    p2 = Agent(2, lossval = -1)
    r1 = Agent(1, learning = False)
    r2 = Agent(2, learning = False)
    r1.epsilon = 1
    r2.epsilon = 1
    series = ['P1-Win','P1-Lose','P1-Draw','P2-Win','P2-Lose','P2-Draw']
    colors = ['r','b','g','c','m','b']
    markers = ['+', '.', 'o', '*', '^', 's']
    perf = [[] for _ in range(len(series) + 1)]
    for i in range(100):
        if i % 10 == 0:
            print('Game: {0}'.format(i))
            probs = measure_performance_vs_random(p1, p2)
            perf[0].append(i)
            for idx,x in enumerate(probs):
                perf[idx+1].append(x)
        winner = play(p1,p2)
        p1.episode_over(winner)
        p2.episode_over(winner)
    while True:
        p2.verbose = True
        p1 = Human(1)
        winner = play(p1,p2)
        p1.episode_over(winner)
        p2.episode_over(winner)