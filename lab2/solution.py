import logging
import numpy as np
from collections import namedtuple
from math import inf
from itertools import chain
from typing import Callable

from utils import *
from gx_utils import *

logging.basicConfig(format="%(message)s", level=logging.INFO)

PROBLEM_SIZE = 500
POPULATION_SIZE = 5
OFFSPRING_SIZE = 3

NUM_GENERATIONS = 100

Individual = namedtuple("Individual", ["genome", "fitness"])

def onemax(genome):
    return sum(genome)


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


def cross_over(g1, g2):
    cut = random.randint(0, PROBLEM_SIZE)
    return g1[:cut] + g2[cut:]


def mutation(g):
    point = random.randint(0, PROBLEM_SIZE - 1)
    return g[:point] + (1 - g[point],) + g[point + 1 :]

def main():
    pass

if __name__ == '__main__':
    main()
