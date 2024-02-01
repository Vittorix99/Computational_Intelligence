import random

from copy import deepcopy
import numpy as np
from game import Game, Move, Player
from collections import namedtuple
from state import GameState, QuixoMove, Move, GameNode, GameTree, NUM_ROWS
from enum import Enum
import itertools
import heuristic_functions as hf
from functools import lru_cache

def map_to_range(num):
    min_source = 1
    max_source = 23
    min_target = 1
    max_target = 5

    if min_source <= num <= max_source:
        return min_target + (num - min_source) / (max_source - min_source) * (max_target - min_target)
    else:
        raise ValueError("Il numero deve essere compreso tra 1 e 23")



class Minimax(Enum):
    MAXIMIXZER = True,
    MINIMIZER = False





class MinimaxPlayer(Player):
    def __init__(self, name, symbol, depth):
        super().__init__()
        self.depth = depth
        self.name = name
        self.symbol = symbol
        self.count = 0


    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:

        winner = game.check_winner() if game.check_winner() != -1 else None
        
        state=  GameState(game._board, game.current_player_idx, winner)
        root = GameNode(True, state, None, state.get_moves(self.symbol),step=0, max_steps= self.depth, )
        tree = GameTree(root, self.depth)

     
        #minimax_move ritorna lo stato con l'evalution migliore mentre best_move rappresenta l'azione da compiere per andare in quello stato
           
        best_state = self.minimax_move(  tree.root, Minimax.MAXIMIXZER,0, self.depth, )
        best_move = best_state.get_action()
        self.count += 1
        
        return best_move
    
    

    
    
    
   

       

    @lru_cache()
    def minimax_move(self, node, maximizing_player, depth= 0, max_depth= 10, ):
            if len(node.children) == 0 or depth>= max_depth:
                score = self.evaluate(node)
                node.value = score
                return score
	
            infinity = float('inf')
            best_val = -infinity
            beta = infinity
            
            successors = node.children
            best_state = None
            for state in successors:
                value = self.min_value(state, best_val, beta, depth+1, max_depth)
                if value > best_val:
                    best_val = value
                    best_state = state
            return best_state

	    
        
    def max_value(self, node, alpha, beta, depth, max_depth):
                    if len(node.children) == 0 or depth>= max_depth:
                         score = self.evaluate(node)
                         node.value = score
                         return score
	
                    infinity = float('inf')
                    value = -infinity

                    successors = node.children
                    for state in successors:
                        value = max(value, self.min_value(state, alpha, beta, depth+1, max_depth))
                        if value >= beta:
                            return value
                        alpha = max(alpha, value)
                    return value

    def min_value(self, node, alpha, beta, depth, max_depth):
            if len(node.children) == 0 or depth>= max_depth:
                score = self.evaluate(node)
                node.value = score
                return score
            infinity = float('inf')
            value = infinity

            successors = node.children
            for state in successors:
                value = min(value, self.max_value(state, alpha, beta, depth+1, max_depth))
                if value <= alpha:
                    return value
                beta = min(beta, value)

            return value

    def evaluate(self, node: GameNode):

        current_state = node.state
        player_symbol = current_state.get_current_player()
        opponent_symbol =  1-player_symbol
        score = 0
        #calcola uno score per gli stati terminali ( lo score è proporzionale al numero di mosse che ha fatto il giocatore che ha vinto)

        winning_score = hf.valuta_winning_score(node, player_symbol, opponent_symbol)   
    
        #calcola uno score per il controllo della scacchiera ( lo score è più alto se le sequenze consecutive di simboli del giocatore corrente sono più lunghe di quelle dell'avversario)
        scacchiera_score = hf.valuta_controllo_scacchiera(current_state)
       
        #calcola uno score per il vantaggio di simboli ( lo score è più alto se il giocatore corrente ha più simboli dell'avversario soprattutto a inizio partita)
        symbol_advantage = hf.valuta_symbol_advantage(current_state.board, player_symbol, opponent_symbol)

        block_score = hf.valuta_blocco_avversario(node, player_symbol, opponent_symbol)

        score = winning_score + scacchiera_score + symbol_advantage + block_score
        return score
    
















        
        



        


        





        
