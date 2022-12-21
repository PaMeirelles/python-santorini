from board import Board
from time import perf_counter

from evaluation import NHS, NHC
from search import get_best_move, negamax


class Controller:
    def __init__(self, time_a, time_b, starting_pos, players):
        self.time = [time_a, time_b]
        self.turn = 1
        self.board = Board(starting_pos)
        self.players = players

        self.evals = []
        self.searches = []
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
                return self.turn * -2
            move.print()
            self.time[index] -= (stop - start)
            self.board.make_move(move)

            if move.end == 3:
                return self.turn
            if self.time[index] < 0:
                return self.turn * -3

            self.turn *= -1
