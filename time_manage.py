# Mother
class TimeManage:
    def __init__(self):
        pass


# Cores
class EstimatedTurnsLeft(TimeManage):
    def __init__(self, a):
        super().__init__()
        self.a = a

    def calculate_time(self, remaining_time, total_time=None, turn=None):
        return remaining_time / self.a


class Phases(TimeManage):
    def __init__(self, phases, m):
        super().__init__()
        self.phases = phases
        self.m = m

    def calculate_time(self, remaining_time, total_time, turn):
        op = False
        phase = 0
        for i, p in enumerate(self.phases):
            if turn >= p:
                phase = i + 1
                if p == self.phases[-1]:
                    op = True
        if op:
            return remaining_time * self.m[phase]
        else:
            return total_time * self.m[phase]


# Implementations
class ETS(EstimatedTurnsLeft):
    def __init__(self):
        super().__init__(15)


class ETP(EstimatedTurnsLeft):
    def __init__(self):
        super().__init__(8)


class ETF(EstimatedTurnsLeft):
    def __init__(self):
        super().__init__(25)


class PHG(Phases):
    def __init__(self):
        super().__init__([4, 8], [0.042, 0.125, 0.25])
