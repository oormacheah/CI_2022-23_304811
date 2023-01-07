import random
import logging
from nim import *
from strategies import *

NIM_SIZE = 15
POPULATION_SIZE = 300
OFFSPRING_SIZE = 300
NUM_GENERATIONS = 1000
TOURNAMENT_SIZE = 2
N_MATCHES = 10
MUTATION_RATE = 0.3

def tournament(population):
    selected_individuals = random.sample(population, k=2)
    
    # The genomes will be put to test playing first and second for N_MATCHES times
    win_count = [0, 0]
    player0 = make_strategy(selected_individuals[0])
    player1 = make_strategy(selected_individuals[1])

    for i in range(N_MATCHES):
        
        # Match 1
        winner = single_match(player0, player1, NIM_SIZE)
        win_count[winner] += 1

        # Match 2
        winner = single_match(player1, player0, NIM_SIZE)
        win_count[winner] += 1
    
    top_g = max(enumerate(win_count), key=lambda y: y[1])[0]

    return top_g

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

# Genetic algorithm

def evolution():

    # Initial population
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
    evolution()