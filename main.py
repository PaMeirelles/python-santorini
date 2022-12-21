from board import Board
from evaluation import NHS
from search import get_best_move

b = Board([7, 11, 13, 17])
b.blocks[11] += 1
b.blocks[6] += 2
b.blocks[12] += 1
e = NHS(b)
s = get_best_move(b, 1, 1, e)