from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match, torney, smart_play, fill_play, mini_match, tour, repair, debut, gen_position
from move import cmp_moves
from search import get_best_move, negamax, alphabeta
from time_manage import ETS
from view import display_pos
from functools import cmp_to_key

repair(180)
# tour("DoomDrop", 180)
smart_play(180)
fill_play(180, on_graph=True)