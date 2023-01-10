from time import perf_counter
from functools import cmp_to_key

PRINT = False
DIVE_CHECK = 100
MAX = 10000


class TtEntry:
    def __init__(self, valid, depth=None, flag=None, value=None):
        self.valid = valid
        self.depth = depth
        self.flag = flag
        self.value = value


def get_best_move(board, turn, eval_func, search_func, time, max_depth=float('inf'), extras=None):
    if extras is None:
        extras = {"Scrapping": False, "Sorting": None}
    best_move = None
    depth = 1
    best_score = -float("inf")
    start = perf_counter()
    counter = 0
    running = True
    if extras["Scrapping"]:
        scores = [-float("inf") for _ in range(len(board.gen_moves(turn)))]
    while perf_counter() - start < time and running and depth < max_depth:
        if not extras["Scrapping"]:
            scores = []
        moves = board.gen_moves(turn)
        if len(moves) == 0:
            best_move, best_score = None, -MAX
            running = False
            continue

        for i, move in enumerate(moves):
            counter += 1
            if counter % DIVE_CHECK == 0:
                if perf_counter() - start > time:
                    if PRINT and extras["Scrapping"]:
                        print(f"{i}/{len(moves)}")
                    running = False
                    break

            board.make_move(move)
            s = -search_func(board, depth - 1, -turn, eval_func,
                             {"alpha": -float("inf"), "beta": float("inf"), "Sorting": extras["Sorting"]})
            if extras["Scrapping"]:
                scores[i] = s
            else:
                scores.append(s)
            board.undo_move(move)

        if len(scores) != 0:
            if not extras["Scrapping"] and not running:
                break
            best_score = max(scores)
            best_move = moves[scores.index(max(scores))]
            if PRINT:
                print(
                    f"Depth: {depth} Score: {eval_func.format_eval(best_score, depth)} Time: {round(perf_counter() - start, 2)}s Move: ",
                    end=" ")
                best_move.pretty_print()
            depth += 1
    return best_move, best_score, depth - 1


def negamax(board, depth, turn, eval_func, extra):
    state = board.get_state()
    if state != 0:
        return (MAX + depth) * state * turn
    if depth == 0:
        return eval_func.eval(board) * turn
    moves = board.gen_moves(turn)
    if len(moves) == 0:
        return -MAX - depth

    scores = []
    for move in moves:
        board.make_move(move)
        scores.append(-negamax(board, depth - 1, -turn, eval_func, extra))
        board.undo_move(move)
    return max(scores)


def alphabeta(board, depth, turn, eval_func, extra):
    alpha = extra["alpha"]
    beta = extra["beta"]
    sorting = extra["Sorting"]
    state = board.get_state()
    if state != 0:
        return (MAX + depth) * state * turn
    if depth == 0:
        return eval_func.eval(board) * turn

    if sorting is not None:
        moves = sorted(board.gen_moves(turn, detailed=True), key=cmp_to_key(sorting))
    else:
        moves = board.gen_moves(turn)

    if len(moves) == 0:
        return -MAX - depth

    score = -float("inf")
    for move in moves:
        board.make_move(move)
        score = max(score, -alphabeta(board, depth - 1, -turn, eval_func,
                                      {"alpha": -beta, "beta": -alpha, "Sorting": sorting}))
        board.undo_move(move)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return score
