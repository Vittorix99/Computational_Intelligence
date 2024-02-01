from game import Game, Move, Player
import time
from ReinforcedPlayer import ReinforcedPlayer
from minimax_player import MinimaxPlayer
import time
from tqdm import tqdm
from minimax_main import play_games, plot_statistics
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
from rl_main import plot_statistics_rl, play_games_rl


if __name__ == '__main__':
   
   

    max_depth = 2
    num_games = 50
    games = 15
    rl_games = 5000
    player1 = ReinforcedPlayer(game_number= num_games)
  
    
    try:
        player1.load()
        print("Loaded ReinforcedPlayer state successfully.")
    except FileNotFoundError:
        print("No saved state found for ReinforcedPlayer. Training from scratch, run rl_main.py first.")
        exit(0)
        
   
    player1 =  MinimaxPlayer("MinimaxPlayer", 0, max_depth)
    player2 =  ReinforcedPlayer(game_number= rl_games)
    player2.load();


    play_games_rl(player1,player2,games,)

    player1 = ReinforcedPlayer(game_number= rl_games)
    player1.load()
    player2 = MinimaxPlayer("Minimax", 1, max_depth)

    play_games_rl(player1,player2,games)




    

