import random 
import numpy as np
import itertools
import lab2_lib as lib
import matplotlib.pyplot as plt
import pickle
from tqdm import tqdm







def initialize_population(population_size):
    return [np.random.randint(2, size=GENOME_SIZE) for _ in range(population_size)]







def elitism(population, fitnesses, elite_size=6):
    sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
    return [individual for individual, _ in sorted_population[:elite_size]]




def mutate(genome, mutation_rate=0.01):
    #mutiamo 1/5 dei geni   
    mutationindices = np.random.choice(len(genome), int(GENOME_SIZE*0.2), replace=False)


    for i in mutationindices:
        if random.random() < mutation_rate:
            genome[i] = 1 - genome[i]
    return genome




def crossover(parent1, parent2, crossover_rate=0.8):
    crossover_point = random.randint(1, GENOME_SIZE - 1)
    if random.random() < crossover_rate:
        child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]]) 
        return child1
    else:
        return parent1


def tournament_selection(population, fitnesses, selection_size=2):
    selected = []
    for _ in range(2):
        indexes =  np.random.choice(len(population), selection_size, replace=False)
        tournament = [(population[i],fitnesses[i]) for i in indexes]
        selected.append(max(tournament, key=lambda x: x[1])[0])

        
    return selected

def roulette_wheel_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probabilities = [f/total_fitness for f in fitnesses]

    # Cumulative probabilities
    #cumulative_probabilities = np.cumsum(selection_probabilities)
    
    # Ruota della fortuna
    selected = []
    for _ in range(2):
        r = np.random.rand()  # Genera un numero casuale tra 0 e 1
        for i, cp in enumerate(selection_probabilities):
            if r <= cp:
                selected.append(population[i])
                break

    return selected


def create_new_population(population, fitnesses, crossover_rate=0.8, mutation_rate=0.01, tournament_size=2, sel_type="tournament", el_size = 6):
    new_population = elitism(population, fitnesses, elite_size=el_size)
    while len(new_population) < len(population):
        parent1, parent2 =  selection_function[sel_type](population, fitnesses, tournament_size) if sel_type == "tournament" else selection_function[sel_type](population, fitnesses)
        child= crossover(parent1, parent2, crossover_rate)
        
        child= mutate(child, mutation_rate)
        new_population.append(child)
    return new_population

def calculate_fitnesses(population, problem):
  fitnesses = []
  for individual in population:
        # Converti l'individuo in una chiave univoca
        key = pickle.dumps(individual)
        
        # Se la fitness di questo individuo è già stata calcolata, usala
        if key in memoization:
            fitness = memoization[key]
        else:
            # Altrimenti, calcola la fitness e memorizzala nel dizionario
            fitness = problem(individual)
            memoization[key] = fitness
            
        fitnesses.append(fitness)
        
  return fitnesses






if __name__ == "__main__":
    instances = [1, 2, 5, 10]
    GENOME_SIZE = 1000
    generations = [150]
    tournament_sizes = [2, 3, 5, 7]
    crossover_rates = [0.4, 0.6, 0.8, 1]
    mutation_rate = 0.15
    population_sizes = [40, 80, 160]
    elite_size = [5, 10, 15] 
    convrgence_generations = 30
    problem_istances = [lib.make_problem(n) for n in instances]
    highest_fitnesses_per_params_combination = {}
    best_configuration_generations = {}

    best_stats_per_instance = {}
    best_generations_per_instance = {}
    memoization = {}
    selection_type = ["tournament", "roulette_wheel"]
    selection_function = {"tournament": tournament_selection, "roulette_wheel": roulette_wheel_selection}
    


  

    for instance, problem in zip(instances, problem_istances):
        highest_fitnesses_per_params_combination = {}   
        best_configuration_generations = {}

        for gen, tournament_size, crossover_rate, population_size, el_size in itertools.product(generations, tournament_sizes, crossover_rates, population_sizes , elite_size):
                    #inizialiiamo la popolazione
                    population = initialize_population(population_size)
                    best_fitness_of_generation = []
                    #best overall è una tupla che contiene il best fitness e il best individual
                    best_overall= (0, [])
                    generation_without_improvement = 0
                    problem._calls = 0
                    #ciclo di generazioni (dato un tournament size, crossover rate e population size)
                    print("==========================================")
                    print(f"GA with tournament size: {tournament_size}, crossover rate: {crossover_rate}, population size: {population_size}, generation: {gen}, elite size : {el_size}")
                    for generation in tqdm(range(gen), desc= "Generation", position=0, leave=True):

                        #calcoliamo il fitness di ogni individuo
                        fitnesses = calculate_fitnesses(population, problem)
                        index_max = max(enumerate(fitnesses), key=lambda x: x[1])[0]
                        #calcoliamo il best fitness e il best individual della generazione  
                        individual_max = population[index_max]
                        fitness_max = fitnesses[index_max]
                        best_fitness_of_generation.append((fitness_max, individual_max))
                    
                       
                        #aggiorniamo il best overall
                        if fitness_max >= best_overall[0]:
                            best_overall = (fitness_max, individual_max)
                            generation_without_improvement = 0 

                        else:
                            #se non abbiamo miglioramenti incrementiamo il contatore
                            generation_without_improvement += 1

                        #se il contatore raggiunge il numero di generazioni di convergenza, usciamo dal ciclo
                        if generation_without_improvement > convrgence_generations:

                            print("End of evolution due to no improvement")
                            print("Max fitness: ", best_overall[0])




                            break

                        
                        #selection and replacement
                        #eseguiamo la selezione e la sostituzione (tournament selection, crossover, mutation)
                        population = create_new_population(population, fitnesses, crossover_rate, mutation_rate, tournament_size, el_size=el_size)
                    
                    #salviamo il best fitness e il best individual e il numero di fitness_calls per ogni combinazione di tournament size, crossover rate e population size
                    key =  ( tournament_size, crossover_rate, population_size, gen, el_size)


                    fitness_calls = problem._calls
                    value = (best_overall[0], best_overall[1], fitness_calls) #salva il best fitness, il best individual e il numero di fitness calls per ogni combinazione di tournament size, crossover rate e population size e numero di generazioni

                    highest_fitnesses_per_params_combination[key] = value
                    #salviamo per ogni configuarazione lo storico dei best fitness 
                    best_configuration_generations[key] = [t[0] for t in best_fitness_of_generation] 



                    print(f"instance: {instance}, tournament_size: {tournament_size}, crossover_rate: {crossover_rate}, population_size: {population_size}, best_fitness: {best_overall[0]}, fitness_calls: {fitness_calls}, elitism size= {el_size}")
        # Trova la chiave con il massimo value[0] ovvero il best fitness
        key_max = max(highest_fitnesses_per_params_combination.keys(), key=lambda x: highest_fitnesses_per_params_combination[x][0])

            # Trova la chiave con il minimo value[2] ovvero il numero minimo di fitness calls
        key_min = min(highest_fitnesses_per_params_combination.keys(), key=lambda x: highest_fitnesses_per_params_combination[x][2])

            # Crea un nuovo dizionario con queste chiavi e i loro corrispondenti valori
        key_stat = instance
        best_stats_per_instance[key_stat]= ( (key_max, highest_fitnesses_per_params_combination[key_max][0]), (key_min, highest_fitnesses_per_params_combination[key_min][2]) )
        best_generations_per_instance[key_stat] = best_configuration_generations[key_max]




    print(best_stats_per_instance)
    print(best_generations_per_instance)


    output_file = open("output.txt", "w")
    output_file.write("==========================================\n")
    output_file.write("Best statistics per instance:\n")
    output_file.write(f" Problem Instance 1: Best Configuration: {best_stats_per_instance[1][0][0]} (Fitness value: {best_stats_per_instance[1][0][1]})\n")
    output_file.write("==========================================\n")
    output_file.write("==========================================\n")
    #output_file.write("Best generations per instance:\n")
    #output_file.write(f" {best_generations_per_instance}")
    output_file.write("==========================================\n")    
    for problem_instance_number, problem in zip(instances, problem_istances):
        best_stats  = best_stats_per_instance[problem_instance_number]
        best_generations = best_generations_per_instance[problem_instance_number]
        best_configuration = best_stats[0][0]
        highest_fitness = best_stats[0][1]
        min_fitness_calls = best_stats[1][1]
        
        if best_configuration:
            plt.figure()
            plt.plot(range(len(best_generations)), best_generations, marker='o')
            title = f"Best Configuration for Problem Instance {problem_instance_number}: Population Size={best_configuration[2]}, Crossover Rate={best_configuration[1]}, Tournament Size={best_configuration[0]}, Max Generations=100 (Fitness value: {highest_fitness}, Fitness Calls: {fitness_calls})"
            plt.title(title, fontsize=10)
            plt.xlabel("Generations")
            plt.ylabel("Best Fitness")
            plt.grid(True)
            plt.savefig(f"best_fitness_problem_number_{problem_instance_number}.png")
            plt.close()
        
        output_file.write(f"the least number of fitness calls for problem instance {problem_instance_number} is {min_fitness_calls} with the following configuration: {best_stats[1][0]}\n")

    output_file.close()






            
            

            




        

                    





        










