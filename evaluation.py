# Mother
from search import MAX


class Eval:
    def __init__(self):
        self.max_eval = None

    def format_eval(self, ev, depth):
        if ev >= MAX:
            return "#" + str((MAX - ev + depth) / 2)
        if ev <= -MAX:
            return "#-" + str((ev + MAX + depth) / 2)
        return round(100 * ev / self.max_eval, 2)


# Cores
class PositionHeight(Eval):
    def __init__(self, a, b, c, func):
        super().__init__()
        self.a = a
        self.b = b
        self.c = c
        self.func = func

    def eval(self, board):
        score = 0
        for i in range(4):
            pl = board.players[i]
            s = self.a * self.b ** board.worker_height(i) + self.c * self.func(pl, board)
            if i <= 1:
                score += s
            else:
                score -= s
        return score


# Implementation
class NeighbourHeight(PositionHeight):
    def __init__(self, a, b, c):
        super().__init__(a, b, c, self.p)

    def p(self, worker, board):
        return len(board.worker_neighbour(worker))


def double_neighbour(square):
    doubles = [9, 12, 15, 12, 9,
               12, 16, 20, 16, 12,
               15, 20, 25, 20, 15,
               12, 16, 20, 16, 12,
               9, 12, 15, 12, 9]
    return doubles[square]


class Double(PositionHeight):
    def __init__(self, a, b, c):
        super().__init__(a, b, c, self.p)

    def p(self, worker, board):
        return double_neighbour(worker)


# Versions
class NHS(NeighbourHeight):
    def __init__(self):
        super().__init__(6, 2, 1)
        self.max_eval = 46


class NHC(NeighbourHeight):
    def __init__(self):
        super().__init__(4, 3, 3)
        self.max_eval = 92


class DBS(Double):
    def __init__(self):
        super().__init__(9, 3, 1)
        self.max_eval = 176
