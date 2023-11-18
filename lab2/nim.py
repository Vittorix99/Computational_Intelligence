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




    