from nim import *
from agent import *

MUTATION_RATE = 0.1
MUTATION_AND_CROSSOVER_RATE = 0.25
NUM_AGENTS = 50
PERFECT_SCORE = (NUM_AGENTS-1) * 2
NUM_STRATEGIES = 6
GOOD_PLAYERS = 0.3
BAD_PLAYERS = 0.3
NUM_ROWS = 4
SELECTION_FACTOR = 5



def population_in( NUM_AGENTS, good_players, bad_players, num_rows):
    # Inizializza la popolazione
    population = []

    # Calcola il numero di "good players"
    num_good_players = int(NUM_AGENTS * good_players)
    num_bad_players = int(NUM_AGENTS * bad_players)
    # Crea i "good players"
    for _ in range(num_good_players):
        strategy_weights = [np.random.uniform(0.5, 0.7), np.random.uniform(0.4, 0.6), np.random.uniform(0.1, 0.2), np.random.uniform(0, 0.2), np.random.uniform(0, 0.2), np.random.uniform(0, 0.2)]
       # np.random.shuffle(strategy_weights)
        genome_move_weights = [np.random.uniform(0, 1) for _ in range(num_rows)]
        genome = (strategy_weights, genome_move_weights)
        population.append(NimAgent(genome))
    for _ in range(num_bad_players):
        strategy_weights = [np.random.uniform(0.1, 0.15), np.random.uniform(0.2, 0.3), np.random.uniform(0.2, 0.4),np.random.uniform(0.4, 0.7), np.random.uniform(0.4, 0.7), np.random.uniform(0.7, 0.9)]
       # np.random.shuffle(strategy_weights)
        genome_move_weights = [np.random.uniform(0, 1) for _ in range(num_rows)]
        genome = (strategy_weights, genome_move_weights)
        population.append(NimAgent(genome))

    # Crea gli altri agenti
    for _ in range(NUM_AGENTS - num_good_players-num_bad_players):
        strategy_weights = [np.random.uniform(0, 1) for _ in range(NUM_STRATEGIES)]
        genome_move_weights = [np.random.uniform(0, 1) for _ in range(num_rows)]
        genome = (strategy_weights, genome_move_weights)
        population.append(NimAgent(genome))

    return population



def crossover( genome1, genome2):
    # Scegli un punto di crossover per ciascuno dei due array nel genoma
    crossover_point1 = np.random.randint(0, len(genome1[0]))
    crossover_point2 = np.random.randint(0, len(genome1[1]))

    # Crea i nuovi genomi scambiando i valori dopo il punto di crossover
    child1_genome = (np.concatenate((genome1[0][:crossover_point1], genome2[0][crossover_point1:])),
                     np.concatenate((genome1[1][:crossover_point2], genome2[1][crossover_point2:])))
    child2_genome = (np.concatenate((genome2[0][:crossover_point1], genome1[0][crossover_point1:])),
                     np.concatenate((genome2[1][:crossover_point2], genome1[1][crossover_point2:])))

    # Crea i nuovi agenti con i genomi creati
    

    return child1_genome, child2_genome


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




def evaluation(population, nim, generation):
    fitness = [0 for _ in range(len(population))]
    average_moves = [0 for _ in range(len(population))]
    # Per ogni agente nella popolazione
    for i, agent1 in enumerate(population):
        # Gioca due volte con ogni altro agente nella popolazione
        for j, agent2 in enumerate(population):
            if i != j:
                # Una volta l'agente inizia per primo
                nim.reset()
                win=0
                agent1.interested = True
                winner, num_moves1, _ = nim.play(agent1, agent2)
                if winner == 1:
                    win += 1
                average_moves[i] += num_moves1

                # Una volta l'agente inizia per secondo
                nim.reset()
                winner, _ ,num_moves2 = nim.play(agent2, agent1)
                
                if winner == 2:
                    win += 1
                
                average_moves[i] += num_moves2

                if win == 2:
                    fitness[i] += 2 
                if win == 0:
                    
                    
                    fitness[i] -= 1
                    

        average_moves[i] /= (len(population) - 1) * 2
        fitness[i] = fitness[i] + generation*2
        fitness[i] -= int(average_moves[i]) 
    return fitness , average_moves

def reproduce(selected):
     new_population = []
     top_percent = selected[:len(selected)//SELECTION_FACTOR]
     while len(new_population)  < len(selected):
            parent1 = random.choice(top_percent)
            parent2 = random.choice(top_percent)
            if random.random() < MUTATION_RATE:
                genome1 = mutate(parent1.genome, MUTATION_RATE)
                genome2 = mutate(parent2.genome, MUTATION_RATE)
                new_population.append(NimAgent(genome1))
                new_population.append(NimAgent(genome2))
            elif random.random()> MUTATION_RATE and random.random() < MUTATION_AND_CROSSOVER_RATE:
                genome1 = mutate(parent1.genome, MUTATION_RATE)
                genome2 = mutate(parent2.genome, MUTATION_RATE)
                child1, child2 = crossover(genome1 , genome2)
                new_population.append(NimAgent(child1))
                new_population.append(NimAgent(child2))
            elif random.random() > MUTATION_AND_CROSSOVER_RATE:
                 child1, child2 = crossover(parent1.genome , parent2.genome)
                 new_population.append(NimAgent(child1))
                 new_population.append(NimAgent(child2))
     return new_population

def selection1(population, fitness):
    # Seleziona gli agenti con fitness più alta

    # Zip population and fitness
    zipped = list(zip(population, fitness))
    # Sort by fitness in descending order
    sorted_population = sorted(zipped, key=lambda x: x[1], reverse=True)
    # Return half of the sorted population
    return [x[0] for x in sorted_population[:len(population)//2]]

def selection2(population, fitness_scores):
    # Logic to select the fittest agents
    # Let's use a simple tournament selection
    selected = []
    while len(selected) < len(population) // 2:
        participant = random.sample(list(zip(population, fitness_scores)), 2)
        winner = max(participant, key=lambda x: x[1])
        selected.append(winner[0])
    return selected

def replacement(population, new_population, fitness_scores):
     half = selection1(population, fitness_scores)
      
     res = half + new_population
     return res



    
    



def evolution_strategy():

    population_init  = population_in(NUM_AGENTS, GOOD_PLAYERS, BAD_PLAYERS, NUM_ROWS)
    generations = 20
    best_fitness = -1 
    nim = Nim(NUM_ROWS)
    bests = []
    for generation in range(generations):
        fitness_scores, average_moves = evaluation(population_init, nim, generation)
        print(f"Generation {generation} completed")
        print(f"Best Fitness: {max(fitness_scores)}")
     
        best_of_generation = population_init[fitness_scores.index(max(fitness_scores))]
        bests.append(best_of_generation)
        print(f"Genome: {best_of_generation.genome}") 
        #print(f"Genome is : {best_agent.genome_strategy}, {best_agent.genome_row}")
        
        #if (max(fitness_scores) >= -PERFECT_SCORE):
            #print(f"Generation {generation} completed")
            #print(f"Best agent: {population_init[fitness_scores.index(max(fitness_scores))]}")
            #best_agent = population_init[fitness_scores.index(max(fitness_scores))] 
            #print(f"Genome is : {best_agent.genome_strategy}, {best_agent.genome_row}")


        selected = selection1(population_init, fitness_scores)

        


        new_population = reproduce(selected)
        
        population_init = replacement(population_init, new_population, fitness_scores)
        
       # print(f"Generation {generation} completed")
        max_fitness = max(fitness_scores)
        
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_agent = best_of_generation
            print(f"Best agent: {best_agent}")
            print(f"Miglior fitness: {max_fitness}")
            
            print(f"Genome is : {best_agent.genome_strategy}, {best_agent.genome_row}")
            

    print(f"Best agent: {best_agent.genome}")
    print(f"Miglior fitness: {max_fitness}")

    fitness_scores, average_moves = evaluation(bests, nim, 0)
    picked = bests[fitness_scores.index(max(fitness_scores))]
    print(f"Genome is : {picked.genome_strategy}, {picked.genome_row}")
    print(f"Fitness: {max(fitness_scores)}")
    print(f"Average moves: {average_moves[fitness_scores.index(max(fitness_scores))]}")
    return picked

    


    











        
      



    








    

    

    



    