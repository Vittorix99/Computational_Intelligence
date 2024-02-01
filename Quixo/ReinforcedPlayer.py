from game import Game, Move, Player
from copy import deepcopy
import numpy as np
import random



class CustomGame(Game):
    def __init__(self, original_game: Game) -> None:
        super().__init__() 
        self._board = original_game.get_board()
        self.current_player_index = original_game.get_current_player()

    def make_move(self, from_position: tuple[int, int], selected_move: Move, player: int) -> None:
        '''Perform a move'''
        if player not in (0, 1):
            return
        previous_value = deepcopy(self._board[(from_position[1], from_position[0])])
        is_acceptable = self.place_piece((from_position[1], from_position[0]), player)
        if is_acceptable:
            is_acceptable = self.shift_pieces((from_position[1], from_position[0]), selected_move)
            if not is_acceptable:
                # restore previous value
                self._board[(from_position[1], from_position[0])] = previous_value
        return is_acceptable
    
    def place_piece(self, from_position: tuple[int, int], player_id: int) -> bool:
        """Checks that {from_position} is in the border and marks the cell with {player_id}"""
        row, col = from_position
        from_border = row in (0, 4) or col in (0, 4)
        if not from_border:
            return False  # the cell is not in the border
        if self._board[from_position] != player_id and self._board[from_position] != -1:
            return False  # the cell belongs to the opponent
        self._board[from_position] = player_id
        return True
    
    def shift_pieces(self, from_position: tuple[int, int], shift: Move) -> bool:
        '''Shift the other pieces'''
        if shift not in self.__valid_shifts(from_position):
            return False  # consider raising ValueError('Invalid argument value')
        axis_0, axis_1 = from_position
        # np.roll performs a rotation of the element of a 1D ndarray
        if shift == Move.RIGHT:
            self._board[axis_0] = np.roll(self._board[axis_0], -1)
        elif shift == Move.LEFT:
            self._board[axis_0] = np.roll(self._board[axis_0], 1)
        elif shift == Move.BOTTOM:
            self._board[:, axis_1] = np.roll(self._board[:, axis_1], -1)
        elif shift == Move.TOP:
            self._board[:(axis_0 + 1), axis_1] = np.roll(self._board[:(axis_0 + 1), axis_1], 1)
        return True
    
    @staticmethod
    def __valid_shifts(from_position: tuple[int, int]):
        """When placing a piece at {from_position} returns the possible shifts"""
        valid_shifts = [Move.BOTTOM, Move.TOP, Move.LEFT, Move.RIGHT]
        axis_0 = from_position[0]    # axis_0 = 0 means uppermost row
        axis_1 = from_position[1]    # axis_1 = 0 means leftmost column

        if axis_0 == 0:  # can't move upwards if in the top row...
            valid_shifts.remove(Move.TOP)
        elif axis_0 == 4:
            valid_shifts.remove(Move.BOTTOM)

        if axis_1 == 0:
            valid_shifts.remove(Move.LEFT)
        elif axis_1 == 4:
            valid_shifts.remove(Move.RIGHT)
        return valid_shifts

def encode_board(board: np.ndarray) -> tuple[int, int]:
    board_1 = np.where(board != -1, 0, board).ravel()
    board_2 = np.where(board != 1, 0, board).ravel()
    value_1 = int(''.join([bin(byte)[2:].rjust(8, '0') for byte in np.packbits(np.where(board_1 == -1, 1, board_1))])[:25], 2)
    value_2 = int(''.join([bin(byte)[2:].rjust(8, '0') for byte in np.packbits(np.where(board_2 == 1, 1, board_2))])[:25], 2)    
    return (value_1, value_2)

def decode_board(board: tuple[int, int]) -> np.ndarray:
    value_1, value_2 = board
    binary_string_1 = format(value_1, 'b').zfill(25)
    binary_string_2 = format(value_2, 'b').zfill(25)
    board_1 = np.array([-int(bit) for bit in binary_string_1])
    board_2 = np.array([int(bit) for bit in binary_string_2])
    return board_1 + board_2

class ReinforcedPlayer(Player):
    def __init__(self, game_number:int, learning_rate: float = 0.1, exploration_rate: float = 0.1, 
                 discount_factor: float = 0.9, exploration_power: int = 5):
        super().__init__()
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.Q = dict()
        self.state = None
        self.action = None
        self.move_sequence = []
        self._moves_used = 0
        self.wins = 0
        self.learning = True
        self.exploration_power = exploration_power
        self.games_played = 0
        self.GAME_NUMBER=game_number
        self.name = "RL"

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        self.state = game.get_board()
        player_is_O = game.get_current_player() == 1

        if player_is_O:
            for i in range(5):
                for j in range(5):
                    self.state[i][j] = (1 - self.state[i][j]) if self.state[i][j] in [0, 1] else self.state[i][j]
        self.state = encode_board(self.state)
        
        if self.state not in self.Q:
            self.Q[self.state] = self.evaluate_moves(game)
            self.action = max(self.Q[self.state], key= lambda k : self.Q[self.state][k])
        else:
            if random.uniform(0, 1) < self.exploration_rate:
                self.action = random.choice(list(self.Q[self.state].keys()))
            else:
                self.action = max(self.Q[self.state], key= lambda k : self.Q[self.state][k])
                self._moves_used += 1
        if self.learning:
            self.move_sequence.append((self.state, self.action))
        return self.action
    
    def update(self, reward: int) -> None:
        for state, action in reversed(self.move_sequence):
            if self.move_sequence.__len__() == 3 and reward == 1:
                self.Q[state][action] = min(1 , self.Q[state][action] + self.learning_rate * (2 *reward * self.Q[state][action]))
            elif reward == 1:
                self.Q[state][action] = min(
                    1 , self.Q[state][action] + self.learning_rate * (reward * self.Q[state][action]))
            else:
                self.Q[state][action] = max(0 , self.Q[state][action] + self.learning_rate * (2 * reward * self.Q[state][action]))
            reward = reward * self.discount_factor
        self.move_sequence = []
        self.games_played += 1

    def evaluate_moves(self, game: Game) -> dict[tuple[tuple[int, int], Move], float]:
        best_moves = {}
        attempts = 0
        while attempts < self.exploration_power:
            temp_game = CustomGame(game)
            from_position = (random.randint(0, 4), random.randint(0, 4))
            move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
            if temp_game.make_move(from_position, move, temp_game.current_player_index):
                attempts += 1
                tmp = self.simulate(temp_game)
                best_moves[(from_position, move)] = tmp
        return best_moves
    
    def simulate(self, game: 'Game') -> float:
        simulation_size = 10
        winner_count = 0
        for _ in range(simulation_size):
            temp_game = deepcopy(game)
            player1 = self.RandomPlayer()
            player2 = self.RandomPlayer()
            winner_count += (temp_game.play(player1, player2) == 0)
        return winner_count / simulation_size

    class RandomPlayer(Player):
        def __init__(self) -> None:
            super().__init__()

        def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
            from_position = (random.randint(0, 4), random.randint(0, 4))
            move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
            return from_position, move

    def stop_learning(self):
        self.learning = False
        self.exploration_rate = 0

    @property
    def moves_used(self):
        return self._moves_used
    
    def save(self):
        np.save(f"reinforced_player_{self.GAME_NUMBER}.npy", self)
    
    def load(self):
        saved_data = np.load(f"reinforced_player_{self.GAME_NUMBER}.npy", allow_pickle=True).item()
        self.Q = saved_data.Q
        self.exploration_rate = saved_data.exploration_rate
        self.learning_rate = saved_data.learning_rate
        self.discount_factor = saved_data.discount_factor
        self.exploration_power = saved_data.exploration_power
        self.games_played = saved_data.games_played
