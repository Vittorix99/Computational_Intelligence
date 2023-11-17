from collections import namedtuple
import numpy as np
 
Nimply = namedtuple("Nimply", "row, num_objects")
class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"
    def reset(self):
        self._rows = [i * 2 + 1 for i in range(len(self._rows))]
    @property
    def rows(self) -> tuple:
        return tuple(self._rows)
    #esegue una mossa di Nim
    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

    
    def play1(self, player1, player2):
        turn = 0
        moves1 = 0
        moves2 = 0
        while self:
          
            if turn == 0:
                ply = player1(self)
                #print(f"ply: player {player1} plays {ply}")
                self.nimming(ply)
                moves1 += 1
            elif turn == 1:
                ply = player2(self)
                #print(f"ply: player {player2} plays {ply}")
                self.nimming(ply)
                moves2 += 1
            turn = 1 - turn
    
        winner = (1-turn) + 1
              
            
        #print(f"status: Player {str(winner)} won!")
        return winner, moves1, moves2
    
    def play(self, player1, player2):
        turn = 0
        moves1 = 0
        moves2 = 0
        while self:
          
            if turn == 0:
                ply = player1.make_move(self)
                #print(f"ply: player {player1} plays {ply}")
                self.nimming(ply)
                moves1 += 1
            elif turn == 1:
                ply = player2.make_move(self)
                #print(f"ply: player {player2} plays {ply}")
                self.nimming(ply)
                moves2 += 1
            turn = 1 - turn
    
        winner = (1-turn) + 1
              
            
        #print(f"status: Player {str(winner)} won!")
        return winner, moves1, moves2


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
    logging.debug(f"analysis:\n{pformat(analysis)}")
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


    