from board import Board
from time import perf_counter

from evaluation import NHS, NHC
from search import get_best_move, negamax


class Controller:
    def __init__(self, time_a, time_b, starting_pos, players):
        self.time = [time_a, time_b]
        self.original_time = [time_a, time_b]
        self.turn = 1
        self.board = Board(starting_pos)
        self.players = players

        self.evals = []
        self.searches = []
        self.moves = []
        self.headers = [[0, 1], starting_pos.copy()]
        self.assembly()

    def assembly(self):
        for player in self.players:
            if player == "Hero":
                self.evals.append(NHS(self.board))
                self.searches.append(negamax)
            elif player == "Sniper":
                self.evals.append(NHC(self.board))
                self.searches.append(negamax)
            else:
                print(f"Engine inválida ({player})")
                exit(1)

    def play_game(self):
        while True:
            if self.turn > 1:
                index = 0
            else:
                index = 1
            start = perf_counter()
            move, score = get_best_move(self.board,
                                        2,
                                        self.turn,
                                        self.evals[index],
                                        self.searches[index])
            stop = perf_counter()
            if score == -float("inf"):
                result = self.turn * -2
                break
            self.moves.append(move)
            move.print()
            self.time[index] -= (stop - start)
            self.board.make_move(move)

            if self.board.blocks[move.end] == 3:
                result = self.turn
                break
            if self.time[index] < 0:
                result = self.turn * -3
                break

            self.turn *= -1

        with open("games/meta", "r") as f:
            n = int(f.read())
        self.write_file(n)
        with open("games/matches", "a") as f:
            f.write(f"{n},{self.players[0]},{self.players[1]},{self.original_time[0]},{self.original_time[1]},{result}\n")
        with open("games/meta", "w") as f:
            f.write(str(n + 1))

    def write_file(self, n):
        with open(f"games/{n}", "x") as f:
            for header in self.headers:
                f.write(" ".join([str(x) for x in header]) + "\n")
            for move in self.moves:
                f.write(move.to_register() + "\n")
