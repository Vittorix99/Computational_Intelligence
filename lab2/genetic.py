from nim import *
from agent import *

MUTATION_RATE = 0.2
MUTATION_AND_CROSSOVER_RATE = 0.4
NUM_AGENTS = 100
num_strategies = 5

def population_init(self, NUM_AGENTS, good_players, bad_players, num_rows):
    # Inizializza la popolazione
    population = []

    # Calcola il numero di "good players"
    num_good_players = int(NUM_AGENTS * good_players)
    num_bad_players = int(NUM_AGENTS * bad_players)
    # Crea i "good players"
    for _ in range(num_good_players):
        strategy_weights = [np.random.uniform(0.6, 0.9), np.random.uniform(0.4, 0.6), np.random.uniform(0, 0.2), np.random.uniform(0, 0.2), np.random.uniform(0, 0.2)]
       # np.random.shuffle(strategy_weights)
        genome_move_weights = [np.random.uniform(0, 1) for _ in range(num_rows)]
        genome = (strategy_weights, genome_move_weights)
        population.append(NimAgent(genome))
    for _ in range(num_bad_players):
        strategy_weights = [np.random.uniform(0.1, 0.2), np.random.uniform(0.2, 0.3), np.random.uniform(0, 0.5), np.random.uniform(0, 0.5), np.random.uniform(0.7, 0.9)]
       # np.random.shuffle(strategy_weights)
        genome_move_weights = [np.random.uniform(0, 1) for _ in range(num_rows)]
        genome = (strategy_weights, genome_move_weights)
        population.append(NimAgent(genome))

    # Crea gli altri agenti
    for _ in range(NUM_AGENTS - num_good_players):
        strategy_weights = [np.random.uniform(0, 1) for _ in range(num_strategies)]
        genome_move_weights = [np.random.uniform(0, 1) for _ in range(num_rows)]
        genome = (strategy_weights, genome_move_weights)
        population.append(NimAgent(genome))

    return population



def crossover(self, parent1, parent2):
    # Scegli un punto di crossover per ciascuno dei due array nel genoma
    crossover_point1 = np.random.randint(0, len(parent1.genome[0]))
    crossover_point2 = np.random.randint(0, len(parent1.genome[1]))

    # Crea i nuovi genomi scambiando i valori dopo il punto di crossover
    child1_genome = (np.concatenate((parent1.genome[0][:crossover_point1], parent2.genome[0][crossover_point1:])),
                     np.concatenate((parent1.genome[1][:crossover_point2], parent2.genome[1][crossover_point2:])))
    child2_genome = (np.concatenate((parent2.genome[0][:crossover_point1], parent1.genome[0][crossover_point1:])),
                     np.concatenate((parent2.genome[1][:crossover_point2], parent1.genome[1][crossover_point2:])))

    # Crea i nuovi agenti con i genomi creati
    child1 = NimAgent(child1_genome)
    child2 = NimAgent(child2_genome)

    return child1, child2


def mutate(genome, mutation_rate):
    # Ensure genome is within bounds after mutation
    mutated_genome = ([], [])
    for i in range(2):
        for j in range(len(genome[i])):
            if random.random() < mutation_rate:
                mutation = random.choice([-1, 1]) * random.random()
                mutated_genome[i].append(min(max(genome[i][j] + mutation, 0), 1))  # Keep genome within [0, 1]
            else:
                mutated_genome[i].append(genome[i][j])
    return mutated_genome




def evaluation(population, nim):
    fitness = [0 for _ in range(len(population))]

    # Per ogni agente nella popolazione
    for i, agent1 in enumerate(population):
        # Gioca due volte con ogni altro agente nella popolazione
        for j, agent2 in enumerate(population):
            if i != j:
                # Una volta l'agente inizia per primo
                nim.reset()
                winner, num_moves1, _ = nim.play(agent1, agent2)
                if winner == 1:
                    fitness[i] += 1 - num_moves1

                # Una volta l'agente inizia per secondo
                nim.reset()
                winner, _ ,num_moves2 = nim.play(agent2, agent1)
                if winner == 2:
                    fitness[i] += 1 - num_moves2


    return fitness

def reproduce(selected):
    new_population = []
    while len(new_population)  < len(selected):
         parent1,parent2 = random.choices(selected, k=2)
         if random.random() < MUTATION_RATE:
            genome1 =(mutate(parent1.genome_strategy, MUTATION_RATE), mutate(parent1.genome_row, MUTATION_RATE))
            genome2 =(mutate(parent2.genome_strategy, MUTATION_RATE), mutate(parent2.genome_row, MUTATION_RATE))
            new_population.append(NimAgent(genome1))
            new_population.append(NimAgent(genome2))
         elif random.random()> MUTATION_RATE and random.random() < MUTATION_AND_CROSSOVER_RATE:
            genome1 =(mutate(parent1.genome_strategy, MUTATION_RATE), mutate(selected[parent1].genome_row, MUTATION_RATE))
            genome2 =(mutate(parent2.genome_strategy, MUTATION_RATE), mutate(selected[parent2].genome_row, MUTATION_RATE))
            child1, child2 = crossover(genome1 , genome2)
            new_population.append(NimAgent(child1))
            new_population.append(NimAgent(child2))
         elif random.random() > MUTATION_AND_CROSSOVER_RATE:
             child1, child2 = crossover(parent1.genoma , parent2.genoma)
             new_population.append(NimAgent(child1))
             new_population.append(NimAgent(child2))
    return new_population