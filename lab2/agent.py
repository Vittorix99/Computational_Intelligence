import random
from copy import deepcopy
import numpy as np
from collections import namedtuple

Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)
    #esegue una mossa di Nim
    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


def nim_sum(state: Nim) -> int:
    tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    xor = tmp.sum(axis=0) % 2
    return int("".join(str(_) for _ in xor), base=2)

class NimAgent:
    def __init__(self, genoma):
        self.genoma = genoma


    def make_move(self, nim_state) -> Nimply:
        optimal_move = self.find_optimal_move( nim_state)
        if optimal_move :
            return optimal_move
        else:
            return self.make_genome_move(nim_state)
        
        
    
    def make_genome_move(self, nim_state):
        moves = [
            (row, min(nim_state.rows[row], max(1, int(self.genome[row] * nim_state.rows[row]))))
            for row in range(len(nim_state.rows)) if nim_state.rows[row] > 0
        ]
        proportional_probs = self.calculate_proportional_probs(nim_state)
        if not proportional_probs:
            return None
        chosen_row = random.choices(range(len(proportional_probs)), proportional_probs)[0]
        nim_move = Nimply(moves[chosen_row][0], moves[chosen_row][1])

        return nim_move


    def optimal_move(self, nim_state):
        for row in range(len(nim_state.rows)):
            for num_objects in range(1, nim_state.rows[row] + 1):
                tmp = deepcopy(nim_state)
                tmp.nimming(Nimply(row, num_objects))
                if nim_sum(tmp) != 0:
                    return Nimply(row, num_objects)
        return None


    def calculate_proportional_probs(self, nim_state):
        total_weight = sum(self.genome)
        proportional_probs = [preference / total_weight for preference in self.genome]







