class Move:
    def __init__(self, who, begin, end, block):
        self.who = who
        self.end = end
        self.begin = begin
        self.block = block

    def pretty_print(self):
        print(f"{self.begin} -> {self.end} ({self.block})")

    def to_register(self):
        return f"{self.who} {self.end} {self.block}"


class Detailed(Move):
    def __init__(self, who, begin, end, block, rise, height, build):
        super().__init__(who, begin, end, block)
        self.rise = rise
        self.height = height
        self.build = build
        groups = [0, 1, 2, 1, 0,
                  1, 2, 3, 2, 1,
                  2, 3, 4, 3, 2,
                  1, 2, 3, 2, 1,
                  0, 1, 2, 1, 0]
        self.center = groups[end] - groups[begin]

    def pretty_print(self):
        print(f"{self.begin} -> {self.end} ({self.block})")
        print(f"Rise: {self.rise}\nHeight:{self.height}\nCenter:{self.center}\nBuild:{self.build}")


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
