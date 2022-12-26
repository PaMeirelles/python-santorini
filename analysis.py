import pandas as pd
from math import log10


def elo_diff(e):
    if e == 0:
        return -800
    if e == 1:
        return 800
    return -400 * log10(1 / e - 1)


def fill_data(time):
    df = pd.read_csv("meta/matches")
    elos = pd.read_csv("elos")
    players = elos["player"]
    data = {p1: {p2: {"wins": 0, "losses": 0, "matches": 0} for p2 in players} for p1 in players}

    for i, row in df.iterrows():
        if row["time_a"] != time:
            continue
        pa, pb = row["player_a"], row["player_b"]
        if row["result"] > 0:
            winner, loser = pa, pb
        else:
            loser, winner = pa, pb

        data[pa][pb]["matches"] += 1
        data[pb][pa]["matches"] += 1

        data[winner][loser]["wins"] += 1
        data[loser][winner]["losses"] += 1

    for p in players:
        with open(f"data/{p}", "w") as f:
            f.write("opponent,wins,losses,matches,eed\n")
            for op in data[p].keys():
                w = data[p][op]['wins']
                l = data[p][op]['losses']
                m = data[p][op]['matches']
                if m != 0:
                    f.write(f"{op},{w},{l},{m},{elo_diff(w/m)}\n")


def adjust_elos(n, new_elos=None):
    if new_elos is None:
        new_elos = {}
    if n == 0:
        with open("elos", "w") as f:
            f.write("player,elo\n")
            for p in new_elos.keys():
                f.write(f"{p},{new_elos[p]}\n")
        return
    elos = pd.read_csv("elos")
    player = elos["player"]
    for p in player:
        df = pd.read_csv(f"data/{p}")
        temp = df.merge(elos, left_on="opponent", right_on="player")
        temp["expected_elo"] = temp["elo"] + temp["eed"]

        d = temp["expected_elo"]
        w = temp["matches"]

        '''print(temp)
        print((d * w).sum() / w.sum())'''
        new_elos[p] = (d * w).sum() / w.sum()
        adjust_elos(n-1, new_elos)


fill_data(180)
adjust_elos(3)