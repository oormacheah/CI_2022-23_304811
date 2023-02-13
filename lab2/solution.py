import logging
import random
from collections import namedtuple

from GA_functions import *

logging.basicConfig(format="%(message)s", level=logging.INFO)

N = 100

POPULATION_SIZE = 1000
OFFSPRING_SIZE = 100
NUM_GENERATIONS = 700
TOURNAMENT_SIZE = 100
MUTATION_RATE = 0.3

GOAL = set(range(N))

Individual = namedtuple("Individual", ["genome", "fitness"])

def main():
    list_of_lists = problem(N, seed=42) # Original problem generation

    list_of_lists = tuple(t for t in set(_ for _ in list_of_lists)) # Remove duplicate lists and cast to tuples

    # Initial population -> random selection and cast to Individuals (not a tournament)
    population = list()
    for _ in range(POPULATION_SIZE):
        subset_list = tuple(random.sample(list_of_lists, k=random.randint(1, len(list_of_lists)))) # Random subset of the lists of lists
        population.append(Individual(subset_list, set_covering_fitness(subset_list)))
    

    # Evolution

    for g in range(NUM_GENERATIONS):
        offspring = list()
        for i in range(OFFSPRING_SIZE):
            if random.random() < MUTATION_RATE:
                p = tournament(population, tournament_size=TOURNAMENT_SIZE)
                o = mutation(p.genome, N)
            else:
                p1 = tournament(population, tournament_size=TOURNAMENT_SIZE)
                p2 = tournament(population, tournament_size=TOURNAMENT_SIZE)
                o = cross_over(p1.genome, p2.genome)
            f = set_covering_fitness(o)
            offspring.append(Individual(o, f))
        population += offspring
        population = sorted(population, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]

    for idx, i in enumerate(population):
        logging.info(f'individual {idx + 1} -> fitness: {i.fitness}, solved problem? {goal_test(i.genome, GOAL)}, w={sum(len(_) for _ in i.genome)}')
    
    

if __name__ == '__main__':
    main()
