import logging
import random
from typing import Callable
from operator import xor
from copy import deepcopy
from itertools import accumulate
from collections import namedtuple


Nimply = namedtuple("Nimply", ['row', 'num_objects'])

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result

def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
        # 'c' is total number of elements per row, 'o' is a number of objects to grab if it's below 'k'
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)
    cooked["sorted_rows"] = sorted(enumerate(state.rows), key=lambda y: y[1]) # My addition
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    cooked["nim_sum"] = nim_sum(state)

    brute_force = list()
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m) # Apply the ply (r, o) -> remove 'o' objects from row 'r' of the current state
        brute_force.append((m, nim_sum(tmp)))
    cooked["brute_force"] = brute_force

    return cooked

def single_match(strategy1, strategy2, nim_size):
    logging.getLogger().setLevel(logging.DEBUG)

    strategy = (strategy1, strategy2)

    nim = Nim(nim_size)
    logging.debug(f"status: Initial board  -> {nim}")
    player = 0 # Initial player
    while nim:
        ply = strategy[player](nim)
        nim.nimming(ply)
        logging.debug(f"status: After player {player} -> {nim}")
        player = 1 - player
    winner = 1 - player
    logging.info(f"status: Player {winner} won!")
    return winner

def evaluate(strategy: Callable, reference_strategy: Callable, NUM_MATCHES: int, NIM_SIZE: int) -> float:
    '''
    Evaluate multiple games against a given strategy (usually nim-sum), your proposed strategy moves first
    '''
    logging.info(f"Evaluating over {NUM_MATCHES} matches on a board of {NIM_SIZE} rows...")

    opponent = (strategy, reference_strategy)
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0 # Setting the passed strategy to perform the first move
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player

        # Exiting the loop, a player has won and it is stored in 'player'

        if player == 1:
            won += 1
    return won / NUM_MATCHES
