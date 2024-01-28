import numpy as np
from copy import deepcopy
from enum import Enum

from collections import namedtuple
QuixoMove = namedtuple('QuixoMove', ['position', 'direction'])

class Move(Enum):
    '''
    Selects where you want to place the taken piece. The rest of the pieces are shifted
    '''
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3



class GameState:
    def __init__(self, board: np.ndarray, current_player: int, winner = None  ):
        self.board = board
        self.current_player = current_player

    def __hash__(self):
        return hash((self.board.tobytes(), self.current_player))

    def __eq__(self, other):
        return self.board == other.board and self.current_player == other.current_player

    def __str__(self):
        for row in self.board:
         board = ' '.join('X' if cell == 0 else 'O' if cell == 1 else '-' for cell in row)

        return f"Board:\n{board}\nCurrent Player: {self.current_player}"

        

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
        for x in range(state._board.shape[0]):
            # if a player has completed an entire row
            if state._board[x, 0] != -1 and all(state._board[x, :] == state._board[x, 0]):
                # return winner is this guy
                winner = state._board[x, 0]
        if winner > -1 and winner != state.get_current_player():
            return winner
        # for each column
        for y in range(state._board.shape[1]):
            # if a player has completed an entire column
            if state._board[0, y] != -1 and all(state._board[:, y] == state._board[0, y]):
                # return the relative id
                winner = state._board[0, y]
        if winner > -1 and winner != state.get_current_player():
            return winner
        # if a player has completed the principal diagonal
        if state._board[0, 0] != -1 and all(
            [state._board[x, x]
                for x in range(state._board.shape[0])] == state._board[0, 0]
        ):
            # return the relative id
            winner = state._board[0, 0]
        if winner > -1 and winner != state.get_current_player():
            return winner
        # if a player has completed the secondary diagonal
        if state._board[0, -1] != -1 and all(
            [state._board[x, -(x + 1)]
             for x in range(state._board.shape[0])] == state._board[0, -1]
        ):
            # return the relative id
            winner = state._board[0, -1]
        return winner
    

    def get_current_player(self) -> int:
        '''
        Returns the current player
        '''
        return deepcopy(self.current_player)
    


    def apply_move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        # In numpy arrays, the first index is the column, the second is the row
        # So, we need to swap the coordinates

        new_state = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable_state = self.__take(new_state,(from_pos[1], from_pos[0]), player_id)
        if acceptable_state!= False:
            acceptable_state = self.__slide(acceptable_state,(from_pos[1], from_pos[0]), slide)
            if acceptable_state != False:
                winner = self.check_winner(acceptable_state) if self.check_winner(acceptable_state) != -1 else None
                acceptable_state.winner = winner  

                return acceptable_state
        return False 
                
            
    @staticmethod
    def __take(self,state,  from_pos: tuple[int, int], player_id: int) -> bool:
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
        ) and (state._board[from_pos] < 0 or state._board[from_pos] == player_id)
        if acceptable:
              state._board[from_pos] = player_id
              return acceptable
              
        return acceptable
    @staticmethod
    
    
    
    def __slide(self, state, from_pos: tuple[int, int], slide: Move) -> bool:
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
            piece = state._board[from_pos]
            # if the player wants to slide it to the left
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    state._board[(from_pos[0], i)] = state._board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                state._board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], state._board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    state._board[(from_pos[0], i)] = state._board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                state._board[(from_pos[0], state._board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    state._board[(i, from_pos[1])] = state._board[(
                        i - 1, from_pos[1])]
                # move the piece up
                state._board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], state._board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    state._board[(i, from_pos[1])] = state._board[(
                        i + 1, from_pos[1])]
                # move the piece down
                state._board[(state._board.shape[0] - 1, from_pos[1])] = piece
        return acceptable
    
    
    def check_move(self, move: QuixoMove) -> bool:
        state = deepcopy(self)
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
        ) and (state._board[move.position] < 0 or state._board[move.position] == state.current_player)

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
        

    def get_moves(self,):
        moves = []
        for row_index, row in enumerate(self.board):
            for column_index, column in enumerate(row):
                for move in Move:
                   quixoMove = QuixoMove((row_index, column_index), move)
                   if self.check_move(quixoMove):
                          moves.append(quixoMove)
        return moves
    