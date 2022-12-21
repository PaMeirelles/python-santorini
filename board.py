class Board:
    def __init__(self):
        self.turn = 0
        self.players = []
        self.blocks = []
        self.vizinhos = [[] for _ in range(25)]
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


b = Board()
print(b.vizinhos)
