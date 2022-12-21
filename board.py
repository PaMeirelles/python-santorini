from move import Move


class Board:
    def __init__(self, players):
        self.turn = 0
        self.players = players
        self.blocks = [0 for _ in range(25)]
        self.vizinhos = [[] for _ in range(25)]
        self.rise = False
        self.stale = False
        self.init_vizinhos()

    def init_vizinhos(self):
        directions = [-6, -5, -4, -1, 1, 4, 5, 6]
        up = (-6, -5, -4)
        down = (4, 5, 6)
        left = (-1, 4, -6)
        right = (1, -4, 6)

        for i in range(25):
            for d in directions:
                if i + d < 0 or i + d > 24:
                    continue
                if d in up and i < 5:
                    continue
                if d in down and i > 20:
                    continue
                if d in left and i % 5 == 0:
                    continue
                if d in right and i % 5 == 4:
                    continue
                self.vizinhos[i].append(i + d)

    def gen_moves(self, turn):
        moves = []
        for i in range(1 - turn, 3 - turn):
            player = self.players[i]
            for v in self.vizinhos[player]:
                if not self.valid_half_move(player, v):
                    continue
                if self.blocks[v] == 3:
                    moves.append(Move(i, player, v, -1))
                    continue
                self.players[i] = -1
                for v2 in self.vizinhos[v]:
                    if self.is_free(v2):
                        moves.append(Move(i, player, v, v2))
                self.players[i] = player
        return moves

    def valid_half_move(self, begin, end):
        if self.blocks[end] - self.blocks[begin] > 1:
            return False
        if not self.is_free(end):
            return False
        return True

    def is_free(self, square):
        if self.blocks[square] == 4:
            return False
        for p in self.players:
            if p == square:
                return False
        return True

    def make_move(self, move):
        self.players[move.who] = move.end
        self.blocks[move.block] += 1
        if self.blocks[move.end] == 3:
            self.rise = True

    def undo_move(self, move):
        self.players[move.who] = move.begin
        self.blocks[move.block] -= 1
        self.rise = False
        self.stale = False

    def worker_height(self, worker):
        return self.blocks[self.players[worker]]

    def worker_neighbour(self, worker):
        return self.vizinhos[worker]

