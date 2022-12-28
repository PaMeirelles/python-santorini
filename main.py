from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match, torney, smart_play, fill_play, mini_match, tour
from search import get_best_move, negamax

fill_play(180, False)
