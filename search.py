from time import perf_counter

DIVE_CHECK = 1
MAX = 10000


def get_best_move(board, turn, eval_func, search_func, time):
    best_move = None
    depth = 1
    best_score = -MAX
    start = perf_counter()
    counter = 0
    while perf_counter() - start < time:
        temp_best_move = None
        temp_best_score = -MAX
        moves = board.gen_moves(turn)
        scores = []

        if len(moves) == 0:
            temp_best_move, temp_best_score = None, -MAX
            continue

        for move in moves:
            counter += 1
            if counter % DIVE_CHECK == 0:
                if perf_counter() - start > time:
                    break
            board.make_move(move)
            scores.append(-search_func(board, depth - 1, -turn, eval_func))
            board.undo_move(move)
        temp_best_move, temp_best_score = moves[scores.index(max(scores))], max(scores)
        print(depth)
        print(perf_counter() - start)
        if temp_best_move is not None:
            temp_best_move.print()
        print(best_score)
        print()
        depth += 1
        best_score = temp_best_score
        best_move = temp_best_move

    return best_move, best_score


def negamax(board, depth, turn, eval_func):
    if depth == 0:
        if board.rise:
            return -(MAX +depth) * turn
        if board.stale:
            return (MAX + depth) * turn

        return eval_func.eval() * turn

    moves = board.gen_moves(turn)
    if len(moves) == 0:
        return 0

    score = -MAX
    for move in moves:
        board.make_move(move)
        score = max(score, -negamax(board, depth - 1, -turn, eval_func))
        board.undo_move(move)

    return score
