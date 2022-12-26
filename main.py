from board import Board
from controller import Controller
from evaluation import NHS
from matches import infinite_match, torney
from search import get_best_move, negamax

'''estranho = [0, 0, 0, 3, 0,
            0, 0, 4, 2, 0,
            0, 3, 0, 0, 0,
            0, 2, 1, 0, 0,
            0, 0, 0, 0, 0]'''
torney(["Lumberjack", "Hero", "Sniper", "Caterpillar", "Hare"], 3 * 60)
'''b = Board([8, 10, 1, 12], estranho)
move, score, depth = get_best_move(b, -1, NHS(), negamax, 1)
print(score)
move.print()'''