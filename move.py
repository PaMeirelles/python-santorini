class Move:
    def __init__(self, who, begin, end, block):
        self.who = who
        self.end = end
        self.begin = begin
        self.block = block

    def print(self):
        print(f"{self.begin} -> {self.end} ({self.block})")