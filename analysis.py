import pandas as pd
import matplotlib.pyplot as plt
from copy import copy
df = pd.read_csv("meta/matches")


def calculate_elo(k, n, time, starting_elos=None):
    if starting_elos is None:
        elos = pd.read_csv("elos")
        starting_elos = {row["player"]: row["elo"] for i, row in elos.iterrows()}
    if n == 0:
        with open("elos", "w") as f:
            f.write("player,elo\n")
            for player in starting_elos.keys():
                f.write(f"{player},{starting_elos[player]}\n")
        return
    players = starting_elos.keys()
    elo_history = [starting_elos]
    for i, row in df.iterrows():
        if row["time_a"] != time:
            continue
        pa, pb = row["player_a"], row["player_b"]
        if row["result"] > 0:
            winner,loser = pa, pb
            r = 1
        else:
            loser,winner = pa, pb
            r = 0
        current_elo = elo_history[-1]
        e = 1 / (1 + 10 ** ((current_elo[pb] - current_elo[pa]) / 400))
        elo_history.append(copy(current_elo))
        new_elo = elo_history[-1]
        d = k * (r - e)
        new_elo[winner] += d
        new_elo[loser] -= d
    for p in players:
        plt.plot([x[p] for x in elo_history], label=p)
    plt.legend()
    #plt.show()
    print(new_elo)
    calculate_elo(k/2, n-1, time, new_elo)


calculate_elo(128, 12, 60)
