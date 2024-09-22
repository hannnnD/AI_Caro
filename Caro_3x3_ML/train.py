from agent import Agent
from player import Human
from gui import emptystate, gameover, DRAW, PLAYER_X, PLAYER_O, EMPTY


def play(agent1, agent2):
    state = emptystate()
    for i in range(9):
        move = agent1.action(state) if i % 2 == 0 else agent2.action(state)
        state[move[0]][move[1]] = (i % 2) + 1
        winner = gameover(state)
        if winner != EMPTY:
            return winner
    return winner

def measure_performance_vs_random(agent1, agent2):
    epsilon1, epsilon2 = agent1.epsilon, agent2.epsilon
    agent1.epsilon, agent2.epsilon = 0, 0
    agent1.learning, agent2.learning = False, False
    r1, r2 = Agent(1), Agent(2)
    r1.epsilon, r2.epsilon = 1, 1
    probs = [0] * 6
    games = 100
    for _ in range(games):
        winner = play(agent1, r2)
        probs[0 if winner == PLAYER_X else 1 if winner == PLAYER_O else 2] += 1.0 / games
    for _ in range(games):
        winner = play(r1, agent2)
        probs[3 if winner == PLAYER_O else 4 if winner == PLAYER_X else 5] += 1.0 / games
    agent1.epsilon, agent2.epsilon = epsilon1, epsilon2
    agent1.learning, agent2.learning = True, True
    return probs

def measure_performance_vs_each_other(agent1, agent2):
    probs = [0, 0, 0]
    games = 100
    for _ in range(games):
        winner = play(agent1, agent2)
        if winner == PLAYER_X:
            probs[0] += 1.0 / games
        elif winner == PLAYER_O:
            probs[1] += 1.0 / games
        else:
            probs[2] += 1.0 / games
    return probs

