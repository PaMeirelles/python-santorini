from time import perf_counter

DIVE_CHECK = 1


def get_best_move(board, turn, eval_func, search_func, time):
    best_move = None
    depth = 1
    best_score = -float("inf")
    start = perf_counter()
    counter = 0
    while perf_counter() - start < time:
        moves = board.gen_moves(turn)
        scores = []

        if len(moves) == 0:
            best_move, best_score = None, float("-inf")
            continue

        for move in moves:
            counter += 1
            if counter % DIVE_CHECK == 0:
                if perf_counter() - start > time:
                    break
            board.make_move(move)
            scores.append(-search_func(board, depth - 1, -turn, eval_func))
            board.undo_move(move)
        depth += 1
        best_move, best_score = moves[scores.index(max(scores))], max(scores)

    return best_move, best_score


def negamax(board, depth, turn, eval_func):
    if depth == 0:
        if board.rise:
            return -float("inf") * turn
        if board.stale:
            return float("inf") * turn

        return eval_func.eval() * turn

    moves = board.gen_moves(turn)
    if len(moves) == 0:
        return 0

    score = -float("inf")
    for move in moves:
        board.make_move(move)
        score = max(score, -negamax(board, depth - 1, -turn, eval_func))
        board.undo_move(move)

    return score
