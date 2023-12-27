import numpy as np
from itertools import product
import pandas as pd
import random
from collections import defaultdict
from tqdm import tqdm
from collections import Counter
import seaborn as sns
from matplotlib import pyplot as plt

#TicTacToe Agent implementation with Reinfocement Learning
class TicTacToe():
    def __init__(self,player = 'X',reward_type ='goal_reward'):
        '''
        player: Role agent should play. If X, agent has the first turn else agent has second turn
        reward_type: 'goal_reward' or 'action_penalty'
        '''
        self.board = np.array(['__']*9).reshape(3,3)
        self.reward_type = reward_type
        self.winning_seqeunce = None #Keep track of winning move made by agent
        self.first_move = None #Keep track of first move made by agent
        if player == 'X':
            self.me ='X'
            self.id = 1
            self.opponent = 'O'
        else:
            self.me = 'O'
            self.id = 2
            self.opponent = 'X'
     
        self.game_over = False #Flag indicating whether game is over
        # Mapping of action representation in board to action representation in tuple 
        self.b_to_s = {'__':0,'X':1,'O':2} 
        # Mapping of action representation in tuple to action representation in board
        self.s_to_b = {0:'__',1:'X',2:'O'} 
        
        #Create mapping from 2D position in board to 1D position in tuple
        positions = self.available_positions()
        self.b2_to_s1 = {position:i for (i,position) in enumerate(positions)}
        
        #Create mapping from 1D position in tuple to 2D position in board 
        self.s1_to_b2 = {i:position for (i,position) in enumerate(positions)}
        
        #State the current player is in
        self.starting_state = self.board_to_state()
        
        #Initialize all possible states of the game
        l_o_l = [list(range(3)) for _ in range(9)]
        states = set(product(*l_o_l))

        #Player X states include states with odd number of blanks and both players have occupied equal number of slots
        #Player O players after Player X, so player O states include states with even number of blanks and where
        #player X has occupied one more slot than player O
        playerX_states = {state for state in states if (state.count(0)%2 == 1 and state.count(1)==state.count(2))} #
        playerO_states =  {state for state in states if (state.count(0)%2 == 0 and state.count(1)==(state.count(2)+1))}

       
        

        #States 
        #self.board_full_states = {state for state in states if state.count(0)==0}
        if player == 'X':
            self.my_states = playerX_states
        else:
            self.my_states = playerO_states
          
    
    def reset_board(self):
        "Function to reset game and reset board to starting state"
        self.board = np.array(['__']*9).reshape(3,3)
        self.starting_state = self.board_to_state()
        self.game_over = False
        self.winning_sequence = None
        self.first_move = None
    
    def show_board(self):    
        "Shows board as a pandas dataframe"
        return pd.DataFrame(self.board)
    
    def board_to_state(self):
        "Convert a board to a state in tuple format"
        return tuple([self.b_to_s[x] for x in np.ravel(self.board)])
    
    @staticmethod
    def possible_actions(state):
        "Return possible actions given a state"
        return [i for i,x  in enumerate(state) if x ==0]
        
    def is_game_over(self):
        "Function to check if game is over"
        if not np.any(self.board == '__') :
            self.game_over = True
            
        return self.game_over
    
    def available_positions(self):
        "Return available positions on the board"
        x,y = np.where(self.board =='__')
        return[(x,y) for x,y in zip(x,y)]
    def opponent_move(self,position):
        "Fills out the board in the given position with the action of the opponent"
        assert position[0] >= 0 and position[0] <= 2 and position[1] >= 0 and position[1] <= 2 , "incorrect position"
        assert self.board[position] == "__" , "position already filled"
        assert np.any(self.board == '__') , "Board is complete"
        assert self.win(self.me) == False and self.win(self.opponent)== False , " Game has already been won"
        self.board[position] = self.opponent
    
    
    def win(self,player):
        "Check if player won the game and record the winning sequence"
        if np.all(self.board[0,:] == player):
            self.winning_sequence = 'R1'
        elif np.all(self.board[1,:] == player): 
            self.winning_sequence = 'R2'
        elif np.all(self.board[2,:] == player):
            self.winning_sequence = 'R3'
        elif np.all(self.board[:,0] == player):
            self.winning_sequence = 'C1'
        elif np.all(self.board[:,1] == player):
            self.winning_sequence = 'C2'
        elif np.all(self.board[:,2] == player):
            self.winning_sequence = 'C3'
        elif np.all(self.board.diagonal()==player):
            self.winning_sequence = 'D1'
        elif  np.all(np.fliplr(self.board).diagonal()==player):
            self.winning_sequence = 'D2'
        else:
            return False
        
        return True
    def my_move(self,position):
        "Fills out the board in the given position with the action of the agent"
        
        assert position[0] >= 0 and position[0] <= 2 and position[1] >= 0 and position[1] <= 2 , "incorrect position"
        assert self.board[position] == "__" , "position already filled"
        assert np.any(self.board == '__') , "Board is complete"
        assert self.win(self.me) == False and self.win(self.opponent)== False , " Game has already been won"
        self.board[position] = self.me
        
        I_win = self.win(self.me)
        opponent_win = self.win(self.opponent)
        
        if self.reward_type == 'goal_reward':
            if I_win:
                self.game_over = True
                return 1
            
            elif opponent_win:
                self.game_over = True
                return -1
            
            else:
                return 0
            
        elif self.reward_type == 'action_penalty':
            if I_win:
                self.game_over = True
                return 0
            
            elif opponent_win:
                self.game_over = True
                return -10
            
            else:
                return -1
    
    def pick_best_action(self, Q, action_type, eps=None, temperature=None):
        """
        Given a Q function, returns the optimal action based on the specified policy.
        
        Args:
            Q: Q-table.
            action_type: Type of action selection policy ('greedy', 'eps_greedy', 'softmax', or 'random').
            eps: Epsilon value for epsilon-greedy policy.
            temperature: Temperature parameter for softmax policy.

        Returns:
            Action: Selected action.
        """
        current_state = self.board_to_state()
        actions = self.possible_actions(current_state)

        # Compute Q values for all possible actions
        Q_values = np.array([Q[current_state][action] for action in actions])

        if action_type == 'greedy':
            chosen_action_index = greedy_policy(Q_values)
        elif action_type == 'eps_greedy':
            assert eps is not None, "Epsilon parameter is required for epsilon-greedy policy"
            chosen_action_index = epsilon_greedy_policy(Q_values, eps)
        elif action_type == 'softmax':
            assert temperature is not None, "Temperature parameter is required for softmax policy"
            softmax_probs = softmax_policy(Q_values, temperature=temperature)
            chosen_action_index = np.random.choice(len(actions), p=softmax_probs)
        elif action_type == 'random':
            chosen_action_index = np.random.choice(len(actions))
        else:
            raise ValueError("Invalid action_type. Supported types are 'greedy', 'eps_greedy', 'softmax', and 'random'.")

        return self.s1_to_b2[actions[chosen_action_index]]


def softmax_policy(Q_values, temperature=1.0):
    """Helper function to calculate softmax probabilities."""
    preferences = Q_values / temperature
    max_preference = np.max(preferences)
    exp_preferences = np.exp(preferences - max_preference)
    softmax_probabilities = exp_preferences / np.sum(exp_preferences)
    return softmax_probabilities    


def greedy_policy(Q_values):
    """Helper function for greedy policy."""
    max_value = np.max(Q_values)
    best_actions = [i for i, q in enumerate(Q_values) if q == max_value]
    return random.choice(best_actions)

def epsilon_greedy_policy(Q_values, eps):
    """Helper function for epsilon-greedy policy."""
    if np.random.random() < eps:
        return np.random.choice(len(Q_values))
    else:
        return greedy_policy(Q_values)






        

