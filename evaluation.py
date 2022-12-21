from board import Board


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

    def eval(self, side):
        score = 0
        for i in range(1 - side, 3 - side):
            s = self.a * self.b ** self.board.worker_height() + self.c * self.func(i)


# Implementation
class NeighbourHeight(PositionHeight):
    def __init__(self, board, a, b, c):
        super().__init__(board, a, b, c, self.func)

    def p(self, worker):
        return len(self.board.worker_neighbour(worker))


# Versions
class NHS(NeighbourHeight):
    def __init__(self, board):
        super().__init__(board, 6, 2, 1)
