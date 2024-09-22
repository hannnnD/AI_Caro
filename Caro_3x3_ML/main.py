from agent import Agent
from player import Human
from train import play, measure_performance_vs_random


if __name__ == "__main__":
    p1 = Agent(1, lossval = -1)
    p2 = Agent(2, lossval = -1)
    r1 = Agent(1, learning = False)
    r2 = Agent(2, learning = False)
    r1.epsilon = 1
    r2.epsilon = 1
    series = ['P1-Win','P1-Lose','P1-Draw','P2-Win','P2-Lose','P2-Draw']
    markers = ['+', '.', 'o', '*', '^', 's']
    perf = [[] for _ in range(len(series) + 1)]
    for i in range(5000):
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