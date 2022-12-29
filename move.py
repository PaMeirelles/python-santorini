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
    def __init__(self, who, begin, end, block, rise, height):
        super().__init__(who, begin, end, block)
        self.rise = rise
        self.height = height
        groups = [0, 1, 2, 1, 0,
                  1, 2, 3, 2, 1,
                  2, 3, 4, 3, 2,
                  1, 2, 3, 2, 1,
                  0, 1, 2, 1, 0]
        self.center = groups[end] - groups[begin]

    def pretty_print(self):
        print(f"{self.begin} -> {self.end} ({self.block})")
        print(f"Rise: {self.rise}\nHeight:{self.height}\nCenter:{self.center}")
