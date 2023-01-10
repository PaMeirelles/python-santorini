import time

import pandas as pd

from board import Board, unhash_blocks, unhash_position
from evaluation import NHS
from move_ordering import cmp_moves, simple_cmp
from search import get_best_move, negamax, alphabeta
from time_manage import ETS


df = pd.read_csv("benchmarking/positions100")
s = df.shape[0]

results = []
for i, row in df.iterrows():
    print(f"{i}/{s}")
    b = Board(unhash_position(row["players"]), blocks=unhash_blocks(row["blocks"]))
    start = time.perf_counter()
    move, score, depth = get_best_move(b,
                                       row['turn'],
                                       NHS(),
                                       alphabeta,
                                       ETS().calculate_time(float('inf'), float('inf'), 0),
                                       max_depth=5, extras={"Scrapping": True, "Sorting": cmp_moves})
    stop = time.perf_counter()
    results.append((score, stop-start))

with open("benchmarking/Librarian_5", "w") as f:
    f.write("score,time\n")
    for r in results:
        f.write(f"{r[0]},{r[1]}\n")

