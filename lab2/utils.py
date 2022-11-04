from itertools import chain
import random

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


class State:
    def __init__(self, data: list):
        self._list = sorted(data.copy())
        self.set_covered = set(chain(*self._list))

    def __hash__(self):
        return hash(tuple(chain(*self._list)))

    def __eq__(self, other):
        return tuple(self.set_covered) == tuple(other.set_covered)

    def __contains__(self, other):
        return set(other) in self.set_covered

    def __le__(self, other):
        return self.set_covered <= other.set_covered

    def __lt__(self, other):
        return self.set_covered < other.set_covered

    def __str__(self):
        return str(chain(*self._list))

    def __repr__(self):
        return repr(self._list)

    def covers(self, other: list):
        return set(other) <= self.set_covered

    @property
    def data(self):
        return self._list

    def copy_data(self):
        return self._list.copy()