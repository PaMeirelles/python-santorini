from board import Board
from time import perf_counter
import datetime
from evaluation import NHS, NHC, DBS
from search import get_best_move, negamax, alphabeta, PRINT
from time_manage import ETS, ETP, ETF


def format_time(time):
    ft = datetime.time(0, int(time // 60), int(time % 60), int(time % 1))
    return ft.strftime("%M:%S") + "." + str(round((time * 10) % 10))


class Controller:
    def __init__(self, time_a, time_b, starting_pos, players, blocks=None):
        self.time = [time_a, time_b]
        self.original_time = [time_a, time_b]
        self.turn = 1
        self.board = Board(starting_pos, blocks)
        self.players = players

        self.evals = []
        self.searches = []
        self.timers = []
        self.extras = []

        self.moves = []
        self.headers = [[0, 1], starting_pos.copy()]
        self.assembly()

    def assembly(self):
        for player in self.players:
            if player == "Hero":
                self.evals.append(NHS())
                self.searches.append(negamax)
                self.timers.append(ETS())
                self.extras.append(None)
            elif player == "Sniper":
                self.evals.append(NHC())
                self.searches.append(negamax)
                self.timers.append(ETS())
                self.extras.append(None)
            elif player == "Caterpillar":
                self.evals.append(NHS())
                self.searches.append(negamax)
                self.timers.append(ETP())
                self.extras.append(None)
            elif player == "Hare":
                self.evals.append(NHS())
                self.searches.append(negamax)
                self.timers.append(ETF())
                self.extras.append(None)
            elif player == "Lumberjack":
                self.evals.append(NHS())
                self.searches.append(alphabeta)
                self.timers.append(ETS())
                self.extras.append(None)
            elif player == "Economist":
                self.evals.append(NHS())
                self.searches.append(alphabeta)
                self.timers.append(ETS())
                self.extras.append({"Scrapping": True})
            elif player == "Gardener":
                self.evals.append(DBS())
                self.searches.append(alphabeta)
                self.timers.append(ETS())
                self.extras.append(None)
            elif player == "Professor":
                self.evals.append(DBS())
                self.searches.append(alphabeta)
                self.timers.append(ETS())
                self.extras.append({"Scrapping": True})
            else:
                print(f"Engine inválida ({player})")
                exit(1)

    def play_game(self):
        while True:
            if self.turn > 0:
                index = 0
            else:
                index = 1
            start = perf_counter()
            move, score, depth = get_best_move(self.board,
                                               self.turn,
                                               self.evals[index],
                                               self.searches[index],
                                               self.timers[index].calculate_time(self.time[index]),
                                               extras=self.extras[index])
            stop = perf_counter()
            if move is None:
                result = self.turn * -2
                break
            self.moves.append(move)
            self.time[index] -= (stop - start)
            if PRINT:
                print(
                    f"Depth:{depth} Eval: {score} Engine: {self.players[index]} Time left: {format_time(self.time[index])}")
            self.board.make_move(move)

            if self.board.blocks[move.end] == 3:
                result = self.turn
                break
            if self.time[index] < 0:
                result = self.turn * -3
                break

            self.turn *= -1

        with open("meta/counter", "r") as f:
            n = int(f.read())
        self.write_file(n)
        with open("meta/matches", "a") as f:
            f.write(
                f"{n},{str(hash_position(self.headers[1]))},{self.players[0]},{self.players[1]},{self.original_time[0]},{self.original_time[1]},{result}\n")
        with open("meta/counter", "w") as f:
            f.write(str(n + 1))
        return result

    def write_file(self, n):
        with open(f"games/{n}", "x") as f:
            for header in self.headers:
                f.write(" ".join([str(x) for x in header]) + "\n")
            for move in self.moves:
                f.write(move.to_register() + "\n")


def hash_position(pos):
    return pos[3] + 25 * pos[2] + 25 ** 2 * pos[1] + 25 ** 3 * pos[0]


def unhash_position(hashed):
    return [hashed // 25 ** 3, (hashed // 25 ** 2) % 25, (hashed // 25) % 25, hashed % 25]

