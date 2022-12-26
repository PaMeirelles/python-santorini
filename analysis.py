import pandas as pd


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
            f.write("opponent,wins,losses,matches\n")
            for op in data[p].keys():
                f.write(f"{op},{data[p][op]['wins']},{data[p][op]['losses']},{data[p][op]['matches']}\n")


fill_data(180)


