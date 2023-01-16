from nim import *
from copy import deepcopy
from functools import cache

def possible_moves(state: Nim):
    # Return a generator
    return (
        Nimply(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    )

@cache
def minimax(state: Nim, maximizingPlayer: bool, depth=None, alpha=-1, beta=1):
    if depth == 0 or not state:
        return 1 if not maximizingPlayer and not state else -1

    scores = []
    for child_ply in possible_moves(state):
        scores.append(
            score := minimax(nimming_new_obj(state, child_ply), not maximizingPlayer, 
                depth - 1 if depth is not None else None, alpha, beta)
        )
        if maximizingPlayer:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
        if beta <= alpha: # In Nim, the case of beta < alpha won't happen (both are either +1 or -1)
            break
        
    return (max if maximizingPlayer else min)(scores)

def minimax_strategy(depth=None, alpha=-1, beta=1) -> Callable:

    def best_possible_move_minimax(state: Nim) -> Nimply:
        return max(
            (minimax(nimming_new_obj(state, child_ply), False, depth=depth, alpha=alpha, beta=beta), child_ply)
            for child_ply in possible_moves(state)
        )[1] # Returns only the ply

    return best_possible_move_minimax