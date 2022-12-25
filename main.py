from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match
from search import get_best_move, negamax
infinite_match("Hero", "Sniper", 3 * 60)