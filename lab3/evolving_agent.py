import random
import logging
from nim import *
from strategies import *
import numpy as np

NIM_SIZE = 4
POPULATION_SIZE = 50
OFFSPRING_SIZE = 30
NUM_GENERATIONS = 100
TOURNAMENT_SIZE = 2
N_MATCHES = 50
MUTATION_RATE = 0.3

Individual = namedtuple("Individual", ["genome"])

def random_genome(genome_length):
    probs = np.array([random.random() for _ in range(genome_length)])
    tot = probs.sum()
    normalized = probs / tot
    return normalized

def tournament(population, tournament_size=2):
    selected_individuals = random.sample(population, k=2)

    # The genomes will be put to test playing first and second for N_MATCHES times
    win_count = [0, 0]
    player0 = make_strategy(selected_individuals[0].genome)
    player1 = make_strategy(selected_individuals[1].genome)

    for i in range(N_MATCHES):
        
        # Match 1
        winner = single_match(player0, player1, NIM_SIZE)
        win_count[winner] += 1

        # Match 2 (inverted order)
        winner = single_match(player1, player0, NIM_SIZE)
        win_count[winner] += 1
    
    top_g = max(enumerate(win_count), key=lambda y: y[1])[0]
    return selected_individuals[top_g]

def cross_over(g1, g2):
    # Particular cross-over
    new_gene = np.empty(5)

    highest1 = max(enumerate(list(g1)), key=lambda x: x[1])[0]
    highest2 = max(enumerate(list(g1)), key=lambda x: x[1])[0]

    if highest1 == highest2:
        # If both share the maximum gene, the maximum is chosen and it is increased at the expense of the others
        current_val1 = g1[highest1]
        current_val2 = g2[highest1]

        max_val = max(current_val1, current_val2)

        added_p = random.random() * max_val
        new_max = max_val + added_p
        new_gene[highest1] = new_max

        # new_gene[highest1] = max_val

        for i in range(len(new_gene)):
            if i != highest1:
                random.seed()
                new_gene[i] = (g1[i], g2[i])[random.choice([0, 1])]
    
    else:
        for i in range(len(new_gene)):
            random.seed()
            new_gene[i] = (g1[i], g2[i])[random.choice([0, 1])]

    norm_gene = np.array([i / new_gene.sum() for i in new_gene])
    return norm_gene


def mutation(g):
    selected = random.choice([[idx, ge] for idx, ge in enumerate(g)]).copy()
    g_copy = g.copy()

    p = random.random()
    if random.random() < 0.5:
        selected[1] -= selected[1] * p
    else:
        selected[1] += selected[1] * p
    
    g_copy[selected[0]] = selected[1]
    norm_gene = np.array([i / sum(g_copy) for i in g_copy])

    return norm_gene
    
# Genetic algorithm

def evolution():
    # Initial population
    population = list()
    for _ in range(POPULATION_SIZE):
        new_genome = random_genome(5)
        population.append(Individual(new_genome))

    # Evolution
    for g in range(NUM_GENERATIONS):
        offspring = list()
        for i in range(OFFSPRING_SIZE):
            if random.random() < MUTATION_RATE:
                p = tournament(population, tournament_size=TOURNAMENT_SIZE)
                o = mutation(p.genome)
            else:
                p1 = tournament(population, tournament_size=TOURNAMENT_SIZE)
                p2 = tournament(population, tournament_size=TOURNAMENT_SIZE)
                o = cross_over(p1.genome, p2.genome)
            offspring.append(Individual(o))
        population += offspring
        population = population[-1::-1][:POPULATION_SIZE]
        random.shuffle(population)

    for idx, i in enumerate(population):
        print(f'individual {idx + 1} -> genome: {[round(n, 3) for n in list(i.genome)]}')

if __name__ == '__main__':
    evolution()