from board import Board
from controller import Controller

print(Board([5, 6, 7, 8]).vizinhos)
c = Controller(3 * 60, 3 * 60, [5, 6, 7, 8], ["Hero", "Hero"])
c.play_game()