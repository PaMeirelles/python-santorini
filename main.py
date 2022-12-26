from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match, torney, smart_play
from search import get_best_move, negamax

# torney(["Gardener", "Hero", "Lumberjack", "Hare", "Caterpillar", "Sniper"], 180, False)
# torney(["Lumberjack", "Gardener", "Economist"], 3 * 60, True)
# infinite_match("Economist", "Lumberjack", 600)
smart_play(180)

