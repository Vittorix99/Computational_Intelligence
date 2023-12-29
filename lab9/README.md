
# Genetic Algorithm Project - README

## Author
The code in this repository was developed with the assistance of Antonio Ferrigno, student number S316467, who contributed to specific sections of the project.

## Code Description
This project implements a genetic algorithm to solve the OneMax problem. The goal is to maximize the fitness function, which is the sum of the values in a binary vector, aiming to have all bits set to 1. Moreover, the algorithm is designed to find parameter configurations that minimize the calls to the fitness function.

In the latest version, a memoization technique has been introduced to store the fitness of individuals that have already been calculated. This enhancement significantly improves the efficiency of the algorithm by avoiding redundant fitness calculations for the same individual.

### Algorithm Parameters
During the execution of the algorithm, the evolutionary algorithm is run with varying parameters:

- **Population Size**: The size of the population of individuals considered during each generation.
- **Tournament Size**: The number of individuals randomly selected from the population to participate in the tournament selection.
- **Convergence Rate**: The convergence percentage that indicates when the algorithm should stop, considering the solution reached as acceptable.
- **Generation**: The number of generations the algorithm should run before terminating. A generation represents a complete cycle of selection, crossover, and mutation of individuals in the population.
