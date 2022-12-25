# Mother
class TimeManage:
    def __init__(self):
        pass


# Cores
class EstimatedTurnsLeft(TimeManage):
    def __init__(self, a):
        super().__init__()
        self.a = a

    def calculate_time(self, remaining_time):
        return remaining_time / self.a


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
