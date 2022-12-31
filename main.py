from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match, torney, smart_play, fill_play, mini_match, tour, repair, debut
from move import cmp_moves
from search import get_best_move, negamax
from view import display_pos
from functools import cmp_to_key

repair(180)
infinite_match("Gardener", "Professor",180)
# debut("Helium", 1200, 180)