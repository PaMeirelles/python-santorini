from random import randint
from controller import Controller


def gen_position():
    n = randint(0, 25 ** 4)
    return [n // 25 ** 3, (n // 25 ** 2) % 25, (n // 25) % 25, n % 25]


def mini_match(player_a, player_b, time):
    result = 0
    pos = gen_position()

    game_1 = Controller(time, time, pos, [player_a, player_b]).play_game()
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
