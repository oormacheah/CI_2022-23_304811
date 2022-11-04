from itertools import chain
from collections import Counter
import random

def goal_test(genome, goal):
    return set(chain(*genome)) == goal

def problem(N, seed=None):
    random.seed(seed)
    return tuple(
        tuple(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    )

def set_covering_fitness(genome):
    c = Counter(tuple(chain(*genome)))

    # Fitness will favor maximum values, so the number of covered elements should be a positive quantity and the bloat, negative.
    return (len(c), len(c) - c.total(), sum(c[e] == 1 for e in c))

def tournament(population, tournament_size=2):
    return max(random.sample(population, k=tournament_size), key=lambda i: i.fitness)

def cross_over(g1, g2):
    cut_percent = random.random() # For the proportional cut
    cut1 = int(cut_percent * len(g1))
    cut2 = int(cut_percent * len(g2))
    return g1[:cut1] + g2[cut2:]

def mutation(g, N):
    outer_point = random.randint(0, len(g) - 1) # Index on the outer list (genome)

    mut_list = g[outer_point] # List selected to be mutated from the genome

    inner_point = random.randint(0, len(mut_list) - 1) # Index of element to be mutated

    # Mutation of the element by adding or subtracting 1 to the randomly chosen element
     
    if mut_list[inner_point] == 0:
        # Force adding 1 if element is 0
        mutated_elem = mut_list[inner_point] + 1
    elif mut_list[inner_point] == (N - 1):
        # Force subtracting 1 if element is N - 1
        mutated_elem = mut_list[inner_point] - 1
    else:
        # If the value is not on the extrema, select either +1 or -1 (randomly)
        mutated_elem = mut_list[inner_point] + random.choice([-1, 1])

    modified_list = mut_list[:inner_point] + (mutated_elem,) + mut_list[inner_point + 1 :]

    return g[:outer_point] + (modified_list,) + g[outer_point + 1 :]
