def get_best_move(board, depth, turn, eval_func, search_func):
    moves = board.gen_moves(turn)
    scores = []

    for move in moves:
        board.make_move(move)
        scores.append(-search_func(board, depth-1, -turn, eval_func))
        board.undo_move(move)
    if len(moves) == 0:
        return None, -float("inf")
    return moves[scores.index(max(scores))], max(scores)


def negamax(board, depth, turn, eval_func):
    if depth == 0:
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
