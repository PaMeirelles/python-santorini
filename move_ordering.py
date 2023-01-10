from move import Detailed


def cmp_moves(move_a, move_b):
    if type(move_a) != Detailed or type(move_b) != Detailed:
        print("Invalid move type")
        return

    # 1st criteria: winning move
    if move_a.height == 3 and move_b.height == 3:
        return 0
    if move_a.height == 3:
        return -1
    if move_b.height == 3:
        return 1

    # 2nd criteria: height diff
    if move_a.rise > move_b.rise:
        return -1
    if move_a.rise < move_b.rise:
        return 1

    # 3rd criteria: built block height
    if move_a.build > move_b.build:
        return -1
    if move_a.build < move_b.build:
        return 1

    # 4th criteria: Centralization
    if move_a.center > move_b.center:
        return -1
    if move_a.center < move_b.center:
        return 1

    return 0


def simple_cmp(move_a, move_b):
    if type(move_a) != Detailed or type(move_b) != Detailed:
        print("Invalid move type")
        return

    # 1st criteria: winning move
    if move_a.height == 3 and move_b.height == 3:
        return 0
    if move_a.height == 3:
        return -1
    if move_b.height == 3:
        return 1

    # 2nd criteria: height diff
    if move_a.rise > move_b.rise:
        return -1
    if move_a.rise < move_b.rise:
        return 1

    # 3th criteria: Centralization
    if move_a.center > move_b.center:
        return -1
    if move_a.center < move_b.center:
        return 1

    return 0
