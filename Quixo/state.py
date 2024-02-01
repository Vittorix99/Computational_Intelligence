import numpy as np
from copy import deepcopy
from enum import Enum
from functools import lru_cache

from game import Move
from collections import namedtuple
QuixoMove = namedtuple('QuixoMove', ['position', 'direction'])



NUM_ROWS = 5

class GameState:
    def __init__(self, board: np.ndarray, current_player: int, winner = None  ):
        self.board = board
        self.current_player = current_player
        self.winner = winner

    def __hash__(self):
        return hash((self.board.tobytes(), self.current_player))

    def __eq__(self, other):
        return self.board == other.board and self.current_player == other.current_player

    def __str__(self):
        for row in self.board:
         board = ' '.join('X' if cell == 0 else 'O' if cell == 1 else '-' for cell in row)

        return f"Board:\n{board}\nCurrent Player: {self.current_player}"

    def print(self):
        '''Prints the board. -1 are neutral pieces, 0 are pieces of player 0, 1 pieces of player 1'''
        for row in self.board:
            print(' '.join('X' if cell == 0 else 'O' if cell == 1 else '-' for cell in row))    

    def __repr__(self):
        return self.__str__()
    
    def __copy__(self):
        return GameState(self.board, self.current_player)
    
    def __deepcopy__(self, memo):
        return GameState(deepcopy(self.board), self.current_player)
    
    def check_winner(self, state) -> int:
        '''Check the winner. Returns the player ID of the winner if any, otherwise returns -1'''
        # for each row
        player = state.get_current_player()
        winner = -1
        for x in range(state.board.shape[0]):
            # if a player has completed an entire row
            if state.board[x, 0] != -1 and all(state.board[x, :] == state.board[x, 0]):
                # return winner is this guy
                winner = state.board[x, 0]
        if winner > -1 and winner != state.get_current_player():
            return winner
        # for each column
        for y in range(state.board.shape[1]):
            # if a player has completed an entire column
            if state.board[0, y] != -1 and all(state.board[:, y] == state.board[0, y]):
                # return the relative id
                winner = state.board[0, y]
        if winner > -1 and winner != state.get_current_player():
            return winner
        # if a player has completed the principal diagonal
        if state.board[0, 0] != -1 and all(
            [state.board[x, x]
                for x in range(state.board.shape[0])] == state.board[0, 0]
        ):
            # return the relative id
            winner = state.board[0, 0]
        if winner > -1 and winner != state.get_current_player():
            return winner
        # if a player has completed the secondary diagonal
        if state.board[0, -1] != -1 and all(
            [state.board[x, -(x + 1)]
             for x in range(state.board.shape[0])] == state.board[0, -1]
        ):
            # return the relative id
            winner = state.board[0, -1]
        return winner
    

    def get_current_player(self) -> int:
        '''
        Returns the current player
        '''
        return deepcopy(self.current_player)
    


    def apply_move(self, mossa:QuixoMove, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        # In numpy arrays, the first index is the column, the second is the row
        # So, we need to swap the coordinates
        
            
        prev_value = deepcopy(self.board[(mossa.position[0], mossa.position[1])])
        new_state = deepcopy(self)
        acceptable_state = self.__take(new_state, (mossa.position[0],mossa.position[1]) , player_id)
        if acceptable_state!= False:
            acceptable_state = self.__slide(new_state,(mossa.position[0],mossa.position[1]), mossa.direction)
            if acceptable_state != False:
                winner = self.check_winner(new_state) 
                if winner == -1:
                    winner = None
                new_state.winner = winner  

                return new_state
        return False 
                
            
    @staticmethod
    def __take(state,  from_pos: tuple[int, int], player_id: int) -> bool:
        '''Take piece'''
        # acceptable only if in border
       
        acceptable: bool = (
            # check if it is in the first row
            (from_pos[0] == 0 and from_pos[1] < 5)
            # check if it is in the last row
            or (from_pos[0] == 4 and from_pos[1] < 5)
            # check if it is in the first column
            or (from_pos[1] == 0 and from_pos[0] < 5)
            # check if it is in the last column
            or (from_pos[1] == 4 and from_pos[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (state.board[from_pos] < 0 or state.board[from_pos] == player_id)
      
        if acceptable:
              state.board[from_pos] = player_id
              return acceptable
              
        return acceptable
    @staticmethod
    
    
    
    def __slide( state, from_pos: tuple[int, int], slide: Move) -> bool:
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = state.board[from_pos]
            # if the player wants to slide it to the left
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    state.board[(from_pos[0], i)] = state.board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                state.board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], state.board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    state.board[(from_pos[0], i)] = state.board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                state.board[(from_pos[0], state.board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    state.board[(i, from_pos[1])] = state.board[(
                        i - 1, from_pos[1])]
                # move the piece up
                state.board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], state.board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    state.board[(i, from_pos[1])] = state.board[(
                        i + 1, from_pos[1])]
                # move the piece down
                state.board[(state.board.shape[0] - 1, from_pos[1])] = piece
        return acceptable
    
    
    def check_move(self,  move: QuixoMove, player) -> bool:
        state = deepcopy(self)
       
       
        if self.check_winner(state) != -1:
            return False
        acceptable_position: bool = (
            # check if it is in the first row
            (move.position[0] == 0 and move.position[1] < 5)
            # check if it is in the last row
            or (move.position[0] == 4 and move.position[1] < 5)
            # check if it is in the first column
            or (move.position[1] == 0 and move.position[0] < 5)
            # check if it is in the last column
            or (move.position[1] == 4 and move.position[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (state.board[move.position] < 0 or state.board[move.position] == player)

        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if move.position not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = move.position[0] == 0 and (
                move.direction == Move.BOTTOM or move.direction == Move.LEFT or move.direction == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = move.position[0] == 4 and (
                move.direction == Move.TOP or move.direction == Move.LEFT or move.direction == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = move.position[1] == 0 and (
                move.direction == Move.BOTTOM or move.direction == Move.TOP or move.direction == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = move.position[1] == 4 and (
                move.direction == Move.BOTTOM or move.direction == Move.TOP or move.direction == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = move.position == (0, 0) and (
                move.direction == Move.BOTTOM or move.direction == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = move.position == (4, 0) and (
                move.direction == Move.TOP or move.direction == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = move.position == (0, 4) and (
                move.direction == Move.BOTTOM or move.direction == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = move.position == (4, 4) and (
                move.direction == Move.TOP or move.direction == Move.LEFT)
        # check if the move is acceptable
        acceptable_slide: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right

        if acceptable_position and acceptable_slide:
            return True
        else:
            return False
        

    def get_moves(self, player):
        moves = []
        for row_index, row in enumerate(self.board):
            for column_index, column in enumerate(row):
                for move in Move:
                   quixoMove = QuixoMove((row_index, column_index), move)
                   if self.check_move(quixoMove, player):
                          moves.append(quixoMove)
        return moves
    

class GameNode:

        def __init__ (self, maximizing_player, state: GameState, action: QuixoMove, available_actions: list[QuixoMove], parent=None, step=0,max_steps= 100,is_terminal=False):
            
            self.state = state
            self.action = action
            self.available_actions = available_actions
            self.parent = parent
            self.children = []
            self.step = step
            self.max_steps = max_steps
            self.is_terminal = False  
            self.Maximize  = maximizing_player


        def add_child(self, child):
            if child not in self.children:
                    self.children.append(child)
            
        def expand(self,):
           if self.Maximize:
               player = self.state.get_current_player()
           else:
                player = 1 - self.state.get_current_player()
            
           if  self.is_terminal == False and self.step <= self.max_steps:
            for action in self.available_actions:
              
                   
                    childstate = self.state.apply_move(action, player)
                    if childstate:
                       
                      
                        
                        terminal = True if childstate.winner != None else False 
                        
                           


                        child = GameNode(True if self.Maximize==False else False, childstate, action, childstate.get_moves(1-player), self, self.step + 1, self.max_steps, terminal )
                        self.add_child(child)
        
            


        def get_action(self):
             return ((self.action.position[1], self.action.position[0]),  self.action.direction)

            


class GameTree:

    def __init__(self, root, depth):
        """
        :param root: root node (GameNode)
        :param depth: desired depth of the game tree

        Constructs a game tree where the root is given and expands it to the given depth.
        """
        self.root = root
        self.expand_tree(self.root, depth)
    
    @lru_cache()
    def expand_tree(self, node, depth):
        """
        Recursively expands the tree from the given node to the specified depth.

        :param node: the node to expand
        :param depth: the remaining depth to expand
        """
        if depth > 0:
            node.expand()
            for child in node.children:
                self.expand_tree(child, depth - 1)
        

    
