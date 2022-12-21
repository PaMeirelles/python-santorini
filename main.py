from board import Board
from controller import Controller

c = Controller(3 * 60, 3 * 60, [5, 6, 7, 8], ["Hero", "Sniper"])
c.play_game()