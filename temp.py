from board import Board

b1 = Board([1, 2, 3, 4])
b2 = Board([2, 3, 4, 5])
b3 = Board([1, 2, 3, 4])

d = {b1: 0}
print(d[b1])
print(d[b3])
print(d[b2])