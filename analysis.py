import pandas as pd
from math import log10
from matplotlib import pyplot as plt
from random import randint

from board import Board, hash_blocks, hash_position
from move import Move


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


def get_positions(n):
    positions = []
    with open("meta/counter", 'r') as f:
        num_games = int(f.read())
    for _ in range(n):
        x = randint(0, num_games)
        with open(f"games/{x}", "r") as m:
            moves = m.readlines()

        b = Board([int(x) for x in moves[1].split()])
        y = randint(2, len(moves))
        for move in moves[2:y]:
            who, to, block = [int(x) for x in move.split()]
            begin = b.players[who]
            b.make_move(Move(who, begin, to, block))

        if y % 2 == 0:
            turn = 1
        else:
            turn = -1
        positions.append({"id": x, "blocks": hash_blocks(b.blocks), "players": hash_position(b.players), "turn": turn})
    with open(f"positions{n}", "w") as f:
        f.write("id,blocks,players,turn\n")
        for pos in positions:
            f.write(f"{pos['id']},{pos['blocks']},{pos['players']},{pos['turn']}\n")


def compare_tests(file_a, file_b):
    plt.style.use('ggplot')

    df_a = pd.read_csv(file_a)
    df_b = pd.read_csv(file_b)

    scores_a = df_a["score"]
    scores_b = df_b["score"]

    times_a = sorted(df_a["time"].apply(lambda x: round(1000 * x, 2)))
    times_b = sorted(df_b["time"].apply(lambda x: round(1000 * x, 2)))
    size = len(scores_a)

    compatibility = [i for i in range(size) if scores_a[i] == scores_b[i]]

    min_a, max_a, avg_a = min(times_a), max(times_a), sum(times_a) / size
    min_b, max_b, avg_b = min(times_b), max(times_b), sum(times_b) / size

    percents_a = [times_a[i * size // 10] for i in range(1, 10)]
    print(percents_a)
    percents_b = [times_b[i * size // 10] for i in range(1, 10)]

    print(f"{file_a} X {file_b}")
    print(f"Score match: {round(100 * len(compatibility)/size, 2)}%")
    print(f"Stats for {file_a}: Min: {min_a}ms Max: {max_a}ms Avg: {round(avg_a, 2)}ms")
    print(f"Stats for {file_b}: Min: {min_b}ms Max: {max_b}ms Avg: {round(avg_b, 2)}ms")

    x = [f"{10 * i}%" for i in range(1, 10)]
    y_a = percents_a
    z_b = percents_b

    x_axis = [i for i in range(1, 10)]

    plt.bar([x - 0.2 for x in x_axis], y_a, 0.4, label=file_a)
    plt.bar([x + 0.2 for x in x_axis], z_b, 0.4, label=file_b)

    plt.xticks(x_axis, x)
    plt.xlabel("Percentiles")
    plt.ylabel("Time")
    plt.title("Time for move search in each percentile")
    plt.legend()
    plt.show()
