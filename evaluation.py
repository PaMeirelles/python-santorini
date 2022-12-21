# Mother
class Eval:
    def __init__(self, board):
        self.board = board


# Cores
class PositionHeight(Eval):
    def __init__(self, board, a, b, c, func):
        super().__init__(board)
        self.a = a
        self.b = b
        self.c = c
        self.func = func

    def eval(self):
        return self.eval_position(1) - self.eval_position(-1)

    def eval_position(self, side):
        score = 0
        for i in range(1 - side, 3 - side):
            pl = self.board.players[i]
            score += self.a * self.b ** self.board.worker_height(i) + self.c * self.func(pl)
        return score


# Implementation
class NeighbourHeight(PositionHeight):
    def __init__(self, board, a, b, c):
        super().__init__(board, a, b, c, self.p)

    def p(self, worker):
        return len(self.board.worker_neighbour(worker))


# Versions
class NHS(NeighbourHeight):
    def __init__(self, board):
        super().__init__(board, 6, 2, 1)


class NHC(NeighbourHeight):
    def __init__(self, board):
        super().__init__(board, 4, 3, 3)
