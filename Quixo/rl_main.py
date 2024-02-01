import random
from game import Game, Move, Player
import time
from ReinforcedPlayer import ReinforcedPlayer
import os
import time
from tqdm import tqdm
from minimax_main import play_games, plot_statistics
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
Statistics = namedtuple('Statistics',['num_steps', 'sequence_count', ])
dict_symbol = {
    0:"X",
    1:"O"
}

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "RandomPlayer"

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


def play_games_rl(player1:Player, player2:Player, num_games:int):
     player1_wins = 0
     player2_wins = 0
    
     num_steps_player1 = []
     num_steps_player2 = []
    
     player1_sequence_dictionary ={}
     player2_sequence_dictionary ={}

     
     for i in tqdm(range(num_games)):
        
        g = Game()
        draws = 0
        
        print(f"Game {i+1} playing.....")
        winner  = g.play(player1, player2)
        g.print()
      

     

        
        
        
        if winner == 0:
           player1_wins += 1
        elif winner == 1:
            player2_wins += 1

     
 
    
         
     filename = f"{player1.name}_vs_{player2.name}_results.txt"
     
     print("================================================================",)
     print(f"Player {player1.name} percentage of wins: {player1_wins/num_games*100}%",)
     print(f"Player {player2.name} percentage of wins: {player2_wins/num_games*100}%",)
     print("================================================================")

     print(f"Num games: {num_games}",)
     print(f"Player {player1.name}: {player1_wins}",)
     print(f"Player {player2.name}: {player2_wins}")
     print("================================================================")
     plot_statistics_rl(player1_wins, player2_wins, player1.name, player2.name, "Risultati delle Partite")
    



def plot_statistics_rl(player_win, opponent_wins,  player_name, opponent_name, title):
    
   

    plt.figure()
    plt.title(title)

    categories = [player_name, opponent_name,]
    values = [player_win, opponent_wins]

    plt.bar(categories, values, color=['blue', 'red'])

    plt.xlabel('Categoria')
    plt.ylabel('Numero di Partite')
    plt.title('Risultati delle Partite')
    plt.xticks(categories, [player_name, opponent_name,])
    plt.savefig(f"{player_name}_vs_{opponent_name}_results.png")
    plt.close()
    
if __name__ == '__main__':
    total_wins = [0, 0]
    game_number= 50
    player1 = ReinforcedPlayer(game_number= game_number)
    player2 = RandomPlayer()
   
    save_filename = f"reinforced_player_{game_number}.npy"

    try:
        player1.load()
        print("Loaded ReinforcedPlayer state successfully.")
    except FileNotFoundError:
        print("No saved state found for ReinforcedPlayer. Training from scratch.")

    if not os.path.exists(save_filename):
        for game_num in tqdm(range(game_number), desc="Playing games", unit="game"):
            g = Game()
            winner, _,_ = g.play(player1, player2)
            total_wins[winner] += 1

        current_time = time.time()
        win_percentage = (total_wins[0] / game_number) * 100
        print(f"Player 1 win percentage: {win_percentage:.2f}%")
        print(f"Player 2 win percentage: {100 - win_percentage:.2f}%")
        print(f"Total time elapsed: {time.time() - current_time} seconds")
        print(f"Average time per game: {(time.time() - current_time) / game_number} seconds")
        player1.save()

    num_games = 50
    total_wins = [0, 0]
    player1 = ReinforcedPlayer(game_number= game_number)
    player2 = RandomPlayer()
    play_games_rl(player1,player2,50)

    play_games_rl(player2,player1,50)

    for game_num in tqdm(range(num_games), desc="Playing games", unit="game"):
            g = Game()
            winner= g.play(player1, player2)
            
            total_wins[winner] += 1

    current_time = time.time()
    win_percentage = (total_wins[0] / num_games) * 100
    print(f"Player 1 win percentage: {win_percentage:.2f}%")
    print(f"Player 2 win percentage: {100 - win_percentage:.2f}%")
    print(f"Total time elapsed: {time.time() - current_time} seconds")
    print(f"Average time per game: {(time.time() - current_time) / num_games} seconds")

    
 



