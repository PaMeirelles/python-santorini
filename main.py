from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match, torney, smart_play, fill_play, mini_match, tour, repair
from move import cmp_moves
from search import get_best_move, negamax
from view import display_pos
from functools import cmp_to_key

mini_match("Helium", "Economist", 1800)