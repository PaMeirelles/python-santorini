import pandas as pd
from math import log10
from matplotlib import pyplot as plt


def elo_diff(e):
    if e == 0:
        return -800
    if e == 1:
        return 800
    return -400 * log10(1 / e - 1)


def fill_data(time):
    df = pd.read_csv("meta/matches")
    elos = pd.read_csv("elos.txt")
    players = elos["player"]
    data = {p1: {p2: {"wins": 0, "losses": 0, "matches": 0} for p2 in players} for p1 in players}
    for i, row in df.iterrows():
        if row["time_a"] != time and time != "any":
            continue
        pa, pb = row["player_a"], row["player_b"]
        if pa == pb:
            continue
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
            f.write("opponent,wins,losses,matches,eed,wr\n")
            for op in data[p].keys():
                w = data[p][op]['wins']
                l = data[p][op]['losses']
                m = data[p][op]['matches']
                if m != 0:
                    f.write(f"{op},{w},{l},{m},{round(elo_diff(w / m), 2)},{round(100 * w / m, 2)}%\n")


def adjust_elos(n, anchor, first=True):
    if n == 0:
        return
    avg = anchor[1]
    new_elos = {}
    elos = pd.read_csv("elos.txt")
    player = elos["player"]
    for p in player:
        df = pd.read_csv(f"data/{p}")
        temp = df.merge(elos, left_on="opponent", right_on="player")
        if first:
            temp["elo"] = avg
        temp["expected_elo"] = temp["elo"] + temp["eed"]

        d = temp["expected_elo"]
        w = temp["matches"]

        '''print(temp)
        print((d * w).sum() / w.sum())'''
        new_elos[p] = (d * w).sum() / w.sum()
        # print(new_elos)
    diff = new_elos[anchor[0]] - anchor[1]
    new_elos = {k: v - diff for k, v in new_elos.items()}
    with open("elos.txt", "w") as f:
        f.write("player,elo\n")
        for p in new_elos.keys():
            f.write(f"{p},{round(new_elos[p], 2)}\n")
    print(f"Adjusting...{n} left")
    return adjust_elos(n - 1, anchor, False)


def match_len(elo=0):
    lens = []
    df = pd.read_csv("meta/matches")
    elos = pd.read_csv("elos.txt")
    remendo = 0
    with open("meta/counter", "r") as f:
        n = int(f.read())

    for i in range(n):
        try:
            with open(f"games/{i}", "r") as f:
                row = df[df.index == i]
                pa, pb = row["player_a"][i - remendo], row["player_b"][i - remendo]
                if int(elos[elos["player"] == pa]["elo"]) < elo:
                    continue
                if int(elos[elos["player"] == pb]["elo"]) < elo:
                    continue
                lens.append(len(f.readlines()) - 1)
        except FileNotFoundError:
            print("not found", i)
        except KeyError:
            print("Matches x games conflict", i)
            remendo += 1
    frequency = {}
    for x in lens:
        if x in frequency.keys():
            frequency[x] += 1
        else:
            frequency[x] = 1
    print(frequency)
    mi = min(frequency.keys())
    ma = max(frequency.keys())
    print("Min", mi)
    print("Max", ma)
    x = [x for x in range(mi, ma + 1) if x in frequency.keys()]
    y = [frequency[x] for x in range(mi, ma + 1) if x in frequency.keys()]
    print("Avg", sum(lens) / len(lens))
    print("Percentile 20%", sorted(lens)[len(lens) // 5])

    plt.plot(x, y)
    plt.show()


def count_matches(time):
    df = pd.read_csv("meta/matches")
    df = df[df["time_a"] == time]
    return df.shape[0]


# match_len(1200)
fill_data(180)
adjust_elos(10, ("Hero", 1000))
print(count_matches(180))
