from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match, torney, smart_play, fill_play, mini_match, tour, repair
from move import cmp_moves
from search import get_best_move, negamax

from functools import cmp_to_key

exemplo = [0, 0, 0, 0, 0,
           0, 0, 0, 0, 0,
           0, 0, 1, 2, 0,
           0, 0, 2, 3, 0,
           0, 0, 0, 0, 0]

players = [11, 12, 7, 17]

b = Board(players, blocks=exemplo)
moves = sorted(b.gen_moves(1, True), key=cmp_to_key(cmp_moves))

for m in moves:
    m.pretty_print()
    print('-' * 50)

# repair(180)