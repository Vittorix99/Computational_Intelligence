import random

from copy import deepcopy
import numpy as np
from game import Game, Move, Player
from collections import namedtuple
from state import GameState, QuixoMove, Move, 
from enum import Enum




class Minimax(Enum):
    MAXIMIXZER = True,
    MINIMIZER = False





class MinimaxPlayer(Player):
    def __init__(self, name, symbol, depth):
        super().__init__(name, symbol)
        self.depth = depth
    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:

        state = game.to_state()
        root = GameNode(state, None, state.get_moves())
        tree = GameTree(root)
        #minimax_move ritorna lo stato con l'evalution migliore mentre best_move rappresenta l'azione da compiere per andare in quello stato
           
        best_state = self.minimax_move(self, root, Minimax.MAXIMIXZER, float('-inf'), float('inf'), is_root=True )
        best_move = best_state.action

        return best_move
    
    
    def minimax_move(self, node, maximizing_player, alpha, beta, is_root=False):
       
       #Condizione di terminazione
        if len(node.children) == 0 or node is None:
           score = self.evaluate(node.state)
           node.value = score
           return score
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            if node is not None:
                successors = node.children()

            
            for child in successors:
                value = self.minimax_move(self, child , Minimax.MINIMIZER, alpha, beta)
                if is_root:
                    if value > max_eval:
                        max_eval = value
                        best_state = child


                else:
                    max_eval = max(max_eval, self.minimax_move(self, child , Minimax.MINIMIZER, alpha, beta))
                    if value >= beta:
                        return value
                    alpha = max(alpha, value) 
            if is_root:
                return best_state
            else:
                return max_eval


           


               
               
               
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move
        else:
            if node is not None:
                successors = node.children()
            min_eval = float('inf')

            for child in successors:
                eval = self.minimax_move(self, child , Minimax.MAXIMIXZER, alpha, beta)
                min_eval = min(min_eval, eval)
                if min_eval<= alpha:
                    return min_eval
                beta = min(beta, eval)
            return min_eval




      
        


        

    
    def evaluate(self, game: Game):

        ##TODO: implementare la funzione di valutazione
        
        pass

    
           





            



class GameNode:

    def __init__ (self, state: GameState, action: QuixoMove, available_actions: list[QuixoMove], parent=None):
        
        self.state = state
        self.action = action
        self.available_actions = available_actions
        self.parent = parent
        self.children = []
        self.score = self.evaluate(self.State)


    def add_child(self, child):
       if self.child not in self.children:
            self.children.append(child)
    
    def expand(self):
       
        for action in self.available_actions:
            if self.state.check_move(action):
                childstate = self.state.apply_move(action)
                child = GameNode(childstate, action, childstate.get_moves(), self)
                self.add_child(child)
        
            





      





class GameTree:

    def __init__(self,  root: GameNode):
        self.root = root
        current_node = root

        current_node.expand()
        if len(current_node.children) > 0:
            for child in current_node.children:
                    child.expand()  



    


