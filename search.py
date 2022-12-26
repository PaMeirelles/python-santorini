from time import perf_counter
from copy import copy

DIVE_CHECK = 1
MAX = 10000


def get_best_move(board, turn, eval_func, search_func, time):
    best_move = None
    depth = 1
    best_score = 100 * -MAX

    start = perf_counter()
    counter = 0
    running = True

    while perf_counter() - start < time and running:
        scores = []
        moves = board.gen_moves(turn)
        if len(moves) == 0:
            best_move, best_score = None, -MAX
            running = False
            continue

        for move in moves:
            counter += 1
            if counter % DIVE_CHECK == 0:
                if perf_counter() - start > time:
                    running = False
                    break

            board.make_move(move)
            scores.append(-search_func(board, depth - 1, -turn, eval_func,
                                       {"alpha": -float("inf"), "beta": float("inf")}))
            board.undo_move(move)

        if len(scores) != 0 and running:
            best_score = max(scores)
            best_move = moves[scores.index(max(scores))]
            depth += 1
    return best_move, best_score, depth-1


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
    state = board.get_state()
    if state != 0:
        return (MAX + depth) * state * turn
    if depth == 0:
        return eval_func.eval(board) * turn
    moves = board.gen_moves(turn)
    if len(moves) == 0:
        return -MAX - depth

    score = -float("inf")
    for move in moves:
        board.make_move(move)
        score = max(score, -alphabeta(board, depth - 1, -turn, eval_func, {"alpha": -beta, "beta": -alpha}))
        board.undo_move(move)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return score
