from gui import printboard, DRAW


class Human(object):
    def __init__(self, player):
        self.player = player

    def action(self, state):
        printboard(state)
        action = input('Nước đi(row, colm): ')
        return (int(action.split(',')[0]), int(action.split(',')[1]))

    def episode_over(self, winner):
        if winner == DRAW:
            print('DRAW')
        else:
            print(f'Game over! Winner: Player {winner}')
