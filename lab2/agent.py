import random
from copy import deepcopy
import numpy as np
from collections import namedtuple
from nim import *



#La fitness è quante volte un agente vince contro un altro agente

#Genome è una tupla di due elementi: il primo array indica i pesi dati a ogni strategia, il secondo array indica quanti oggetti sottrarre dall i-esima riga







class NimAgent:
    def __init__(self, genoma, interested = False):
        self.genome_strategy = genoma[0]
        self.genome_row = genoma[1]
        self.strategy = self.choose_strategy()
        self.interested = interested
        self.genome= genoma


    def __str__(self):
          if self.interested:
            return "Player sotto esame:" +  self.strategy.__name__
          else:
            return "Second Player:" +  self.strategy.__name__
                

                    

    def make_move(self, nim_state) -> Nimply:
            
            strategy = self.choose_strategy()
            self.strategy = strategy
            return strategy(nim_state)
            #return self.strategy(nim_state)


    def choose_strategy(self):
            # Definisci le strategie disponibili
            strategies = [self.optimal_move, self.make_genome_move, self.select_min_row, self.select_odd_row, self.select_even_row, self.random_move]

            # Normalizza i valori nel genoma per farli sommare a 1
            genome_sum = sum(self.genome_strategy)
            probabilities = [value / genome_sum for value in self.genome_strategy]

            # Scegli una strategia in base alle probabilità
            strategy = random.choices(strategies, weights=probabilities, k=1)[0]

            return strategy



    def random_move(self, nim_state):
            # Trova gli indici delle pile che non sono vuote
            non_empty_piles = [i for i, num in enumerate(nim_state._rows) if num > 0]

            # Scegli una pila a caso tra quelle non vuote
            pile_index = random.choice(non_empty_piles)

            # Scegli un numero a caso di oggetti da rimuovere da quella pila
            num_objects = random.randint(1, nim_state._rows[pile_index])

            return Nimply(pile_index, num_objects)
    def select_min_row(self, nim_state):
            # Trova l'indice della pila con il minor numero di oggetti
            nim_state = nim_state._rows
            min_pile_index = nim_state.index(min(i for i in nim_state if i > 0))

            # Se c'è solo una pila con più di 0 oggetti, rimuovi tutti gli oggetti da quella pila
            if nim_state.count(0) == len(nim_state) - 1:
                num_objects = nim_state[min_pile_index]
            else:
                # Altrimenti, rimuovi un solo oggetto dalla pila
                num_objects = 1

            return Nimply(min_pile_index, num_objects)
        

        
    def select_max_row(self, nim_state):
        # Trova l'indice della pila con il maggior numero di oggetti
                nim_state = nim_state._rows
                max_pile_index = nim_state.index(max(nim_state))

                # Se c'è solo una pila con più di 0 oggetti, rimuovi tutti gli oggetti da quella pila
                if nim_state.count(0) == len(nim_state) - 1:
                    num_objects = nim_state[max_pile_index]
                
                else:
                    # Altrimenti, rimuovi il numero massimo d i oggetti disponibili - 1
                    num_objects = nim_state[max_pile_index] - 1 if nim_state[max_pile_index] > 1 else 1

                return Nimply(max_pile_index, num_objects)
        
    def select_odd_row(self, nim_state):
            # Trova gli indici delle pile con un numero dispari di oggetti
            nim_state = nim_state._rows
            max_pile_index = nim_state.index(max(nim_state))

                # Se c'è solo una pila con più di 0 oggetti, rimuovi tutti gli oggetti da quella pila
            if nim_state.count(0) == len(nim_state) - 1:
                    num_objects = nim_state[max_pile_index]
                    return Nimply(max_pile_index, num_objects)

            odd_pile_indices = [i for i, num in enumerate(nim_state) if i % 2 == 1 and num > 0]

            if odd_pile_indices:
                # Se ci sono pile con un numero dispari di oggetti, scegli una di queste pile e rimuovi un oggetto
                pile_index = random.choice(odd_pile_indices)
                num_objects = 1
            else:
                # Altrimenti, scegli una pila a caso e rimuovi un elemento da quella pila
                pile_index = random.choice([i for i, num in enumerate(nim_state) if num > 0])
                num_objects = 1

            return Nimply(pile_index, num_objects)
        
    def select_even_row(self, nim_state):
            # Trova gli indici delle pile con un numero massimo di oggetti
            nim_state = nim_state._rows
            max_pile_index = nim_state.index(max(nim_state))

            # Se c'è solo una pila con più di 0 oggetti, rimuovi tutti gli oggetti da quella pila
            if nim_state.count(0) == len(nim_state) - 1:
                num_objects = nim_state[max_pile_index]
                return Nimply(max_pile_index, num_objects)

            even_pile_indices = [i for i, num in enumerate(nim_state) if num > 0 and i % 2 == 0]

            if even_pile_indices:
                # Se ci sono pile con un numero dispari di oggetti, scegli una di queste pile e rimuovi un oggetto
                pile_index = random.choice(even_pile_indices)
                num_objects = 1
            else:
                # Altrimenti, scegli una pila a caso e rimuovi un elemento da quella pila
                pile_index = random.choice([i for i, num in enumerate(nim_state) if num > 0])
                num_objects = 1

            return Nimply(pile_index, num_objects)
    
    def make_genome_move(self, nim_state):
            moves = [
                (row, min(nim_state._rows[row], max(1, int(self.genome_row[row] * nim_state._rows[row]))))
                for row in range(len(nim_state._rows)) if nim_state._rows[row] > 0
            ]
            proportional_probs = self.calculate_proportional_probs(nim_state)
            if not proportional_probs:
                return None
            #chosen_row = random.choices(range(len(proportional_probs)), proportional_probs)[0]
            chosen_move = max(moves, key=lambda x: self.genome_row[x[0]])
            nim_move = Nimply(chosen_move[0], chosen_move[1])

            return nim_move


    def optimal_move(self, nim_state):
            for row in range(len(nim_state._rows)):
                for num_objects in range(1, nim_state._rows[row] + 1):
                    tmp = deepcopy(nim_state)
                    tmp.nimming(Nimply(row, num_objects))
                    if nim_sum(tmp) == 0:
                        return Nimply(row, num_objects)
            return self.make_genome_move(nim_state)


    def calculate_proportional_probs(self, nim_state):
        total_weight = sum(self.genome_row)
        proportional_probs = [preference / total_weight for preference in self.genome_row ]
        return proportional_probs


    
def nim_sum(state: Nim) -> int:
    tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    xor = tmp.sum(axis=0) % 2
    return int("".join(str(_) for _ in xor), base=2)


def analize(raw: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = dict()
    for ply in (Nimply(r, o) for r, c in enumerate(raw.rows) for o in range(1, c + 1)):
        tmp = deepcopy(raw)
        tmp.nimming(ply)
        cooked["possible_moves"][ply] = nim_sum(tmp)
    return cooked


def optimal(state: Nim) -> Nimply:
    analysis = analize(state)
   # logging.debug(f"analysis:\n{pformat(analysis)}")
    spicy_moves = [ply for ply, ns in analysis["possible_moves"].items() if ns != 0]
    if not spicy_moves:
        spicy_moves = list(analysis["possible_moves"].keys())
    ply = random.choice(spicy_moves)
    return ply

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def adaptive(state: Nim) -> Nimply:
    """A strategy that can adapt its parameters"""
    genome_row = np.load("genome_row.npy")
    genome_strategy = np.load("genome_strategy.npy")
    genome = ([1,0,0,0,0,0], genome_row)

    agent = NimAgent(genome)
    return agent.make_move(state)


def pure_random(state: Nim) -> Nimply:
    """A completely random move"""
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)





