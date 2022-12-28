from random import randint, shuffle

from analysis import fill_data
from controller import Controller
from search import PRINT
import pandas as pd


def gen_position():
    while True:
        n = randint(0, 25 ** 4)
        a, b, c, d = n // 25 ** 3, (n // 25 ** 2) % 25, (n // 25) % 25, n % 25
        if len({a, b, c, d}) != 4:
            continue
        return [a, b, c, d]


def mini_match(player_a, player_b, time):
    result = 0
    pos = gen_position()
    if PRINT:
        print(pos)
    print(f"{player_a} x {player_b}")
    game_1 = Controller(time, time, pos, [player_a, player_b]).play_game()
    print(f"{player_b} x {player_a}")
    game_2 = Controller(time, time, pos,
                        [player_b, player_a]).play_game()

    if game_1 > 0:
        result += 1
    if game_2 < 0:
        result += 1

    return result


def infinite_match(player_a, player_b, time):
    played = 0
    result = 0

    while True:
        result += mini_match(player_a, player_b, time)
        played += 2
        print(f"{player_a} {result} x {played - result} {player_b}")


def torney(players, time, sh):
    if sh:
        shuffle(players)
    while True:
        scores = [0 for _ in range(len(players))]
        for p1 in range(len(players)):
            for p2 in range(p1 + 1, len(players)):
                result = mini_match(players[p1], players[p2], time)
                scores[p1] += result
                scores[p2] += (2 - result)
        for i in range(len(players)):
            print(f"{players[i]} - {scores[i]}")
        print()


def smart_play(time):
    fill_data(time)
    elos = pd.read_csv("elos")
    player = elos["player"]
    for p in player:
        df = pd.read_csv(f"data/{p}")
        temp = df.merge(elos, left_on="opponent", right_on="player")
        for i, row in temp.iterrows():
            if row["wins"] == 0 or row["losses"] == 0:
                mini_match(p, row["opponent"], time)
                smart_play(time)


def fill_play(time, any_time=True):
    if any_time:
        fill_data("any")
    else:
        fill_data(time)
    elos = pd.read_csv("elos")
    player = elos["player"]

    lower_matches = float('inf')
    pa = None
    pb = None

    for p in player:
        df = pd.read_csv(f"data/{p}")
        temp = df.merge(elos, left_on="opponent", right_on="player")
        for i, row in temp.iterrows():
            if row["opponent"] == p:
                continue
            if row["matches"] < lower_matches:
                lower_matches = row["matches"]
                pa = p
                pb = row["opponent"]
    print(f"Matches: {lower_matches}")
    mini_match(pa, pb, time)
    fill_play(time, False)


def tour(player, time):
    elos = pd.read_csv("elos")
    players = elos["player"]
    for p in players:
        if p != player:
            mini_match(player, p, time)