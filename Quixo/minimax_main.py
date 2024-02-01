import random
from game2 import Game, Move, Player
from minimax_player import MinimaxPlayer
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np 
import os  
from tqdm import tqdm
Statistics = namedtuple('Statistics',['num_steps', 'sequence_count', ])
dict_symbol = {
    0:"X",
    1:"O"
}

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "RandomPlayer"
        self.count = 0

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        
        return from_pos, move




def play_games(player1:Player, player2:Player, num_games:int):
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
        winner, sequence, draw  = g.play(player1, player2)
        g.print()
        if sequence["type"] == "r" or sequence["type"] == "c":
            key = (sequence["type"], sequence["index"])
        else:
            key = (sequence["type"]) 

        count_player1 = g.moves_count
        count_player2 = g.moves_count
        
        if winner==0:
            num_steps_player1.append(count_player1)
            if key in player1_sequence_dictionary:
                num_steps_line_1 = player1_sequence_dictionary[key].num_steps
            else:
                num_steps_line_1 = []
            num_steps_line_1.append(count_player1)

            player1_sequence_dictionary[key] = Statistics(num_steps_line_1, player1_sequence_dictionary[key].sequence_count+1 if key in player1_sequence_dictionary else 1)
        
        elif winner==1:
            num_steps_player2.append(count_player2)
            if key in player2_sequence_dictionary:
                num_steps_line_2 = player2_sequence_dictionary[key].num_steps
            else:
                num_steps_line_2 = []
            
            num_steps_line_2.append(count_player2)



            player2_sequence_dictionary[key] = Statistics(num_steps_line_2 , player2_sequence_dictionary[key].sequence_count + 1 if key in player2_sequence_dictionary else 1)
            num_steps_player2.append(count_player2)

        
        
        
        if winner == 0:
           player1_wins += 1
        elif winner == 1:
            player2_wins += 1

        elif draw:
           draws = draws + 1
    
     total_steps = 0
     total_entries = 0

     for key in player1_sequence_dictionary.keys():
        num_steps_list = player1_sequence_dictionary[key].num_steps
        if num_steps_list:  # Assicurati che la lista non sia vuota
            total_steps += sum(num_steps_list)
            total_entries += len(num_steps_list)
            player1_sequence_dictionary[key] = Statistics(total_steps/total_entries, player1_sequence_dictionary[key].sequence_count)

     total_steps = 0
     total_entries = 0
     for key in player2_sequence_dictionary.keys():
         num_steps_list = player2_sequence_dictionary[key].num_steps
         if num_steps_list:  # Assicurati che la lista non sia vuota
             total_steps += sum(num_steps_list)
             total_entries += len(num_steps_list)
             player2_sequence_dictionary[key] = Statistics(total_steps/total_entries, player2_sequence_dictionary[key].sequence_count)

    

     filename = f"{player1.name}_vs_{player2.name}_results.txt"
     print("================================================================")
     print(f"Player {player1.name} percentage of wins: {player1_wins/num_games*100}%")
     print(f"Player {player2.name} percentage of wins: {player2_wins/num_games*100}%")
     print(f"Draw percentage: {draws/num_games*100}%")
     print("================================================================")

     print(f"Num games: {num_games}")
                
     print(f"Player {player1.name}: {player1_wins}")
     print(f"Player {player2.name}: {player2_wins}")
     print("================================================================")
     if len(num_steps_player1) > 0:
                    print(f"Player1 {player1.name} - Average num steps: {sum(num_steps_player1)/len(num_steps_player1)}")
                    print(f"Player1 {player1.name} - Max num steps:{max(num_steps_player1)}")
                    print(f"Player1 {player1.name} - Min num steps : {min(num_steps_player1)}")
     print(f"Player1 {player1.name} Number of draws: {draws}")
     print("================================================================")
     if len(num_steps_player2) > 0:
                    print(f"Player2 {player2.name} - Average num steps: {sum(num_steps_player2)/len(num_steps_player2)}")
                    print(f"Player2 {player2.name} - Max num steps: {max(num_steps_player2)}")
                    print(f"Player2 {player2.name} - Min num steps : {min(num_steps_player2)}")
     print(f"Player2 {player2.name} Number of draws: {draws}")
     print("================================================================")
     plot_statistics(player1_wins, player2_wins, draws, num_steps_player1, player1_sequence_dictionary, player1.name, player2.name, title=f"{player1.name} {dict_symbol[0]} vs {player2.name} {dict_symbol[1]}" ) 
     plot_statistics(player2_wins, player1_wins, draws, num_steps_player2, player2_sequence_dictionary, player2.name, player1.name, title=f"{player1.name} {dict_symbol[0]} vs {player2.name} {dict_symbol[1]}" )

def plot_statistics(player_win, opponent_wins, draws, player_steps,  player_sequences, player_name, opponent_name, title):
    
    keys = list(player_sequences.keys())
    sequence_counts = [stats.sequence_count for stats in player_sequences.values()]
    num_steps = [stats.num_steps for stats in player_sequences.values()]

    # Larghezza delle barre
    bar_width = 0.26
    bar_steps_width = 0.15

    # Creazione di un grafico
    fig, ax = plt.subplots()

    # Posizioni delle barre
    indices = np.arange(len(keys))

    # Barre per sequence_count
    bar1 = ax.bar(indices - bar_width/2, sequence_counts, bar_width, label='Conteggio linea di vittoria')

    # Barre per num_steps
    bar2 = ax.bar(indices + bar_width/2, num_steps, bar_steps_width, label='Numero medio di passi')


    #add_values_on_bars(ax, 5)
    # Etichette e titolo
    ax.set_xlabel('Linea')
    ax.set_ylabel('Valore')
    
    ax.set_title(f'{title}_Player {player_name}_Victory lines')
    ax.set_xticks(indices)
    ax.set_xticklabels(keys)
    ax.legend()


    # Salvataggio e chiusura
    plt.savefig(f"{title}_{player_name}_victory_lines_count.png")

    plt.close(fig)
    
    plt.figure()

    #Plotta la frerquenza del  numero di passi per la vittoria
    if len(player_steps) > 0:
        plt.figure(figsize=(14, 14))
        plt.hist(player_steps, bins=range(min(player_steps), max(player_steps) + 2), edgecolor='black', align='left')

        plt.xlabel('Numero di Passi per la Vittoria')
        plt.ylabel('Frequenza')
        plt.title('Distribuzione dei Passi per la Vittoria')
        plt.xticks(range(min(player_steps), max(player_steps) + 1), rotation=90)  # Etichette sull'asse x per ogni numero di passi

        plt.savefig(f"{title}_{player_name}_victory_steps.png")  # Salvataggio e chiusura
        plt.close()

    plt.figure()
    plt.title(title)

    categories = [player_name, opponent_name, 'Draws']
    values = [player_win, opponent_wins, draws]

    plt.bar(categories, values, color=['blue', 'red', 'green'])

    plt.xlabel('Categoria')
    plt.ylabel('Numero di Partite')
    plt.title('Risultati delle Partite')
    plt.xticks(categories, [player_name, opponent_name, 'Draws'])
    plt.savefig(f"{player_name}_vs_{opponent_name}_results.png")
    plt.close()
    


def add_values_on_bars(axes, spacing=5):
    for bar in axes.patches:
        axes.annotate(f"{bar.get_height()}", 
                     (bar.get_x() + bar.get_width() / 2, 
                      bar.get_height()), 
                     ha='center', va='bottom',
                     xytext=(0, spacing),
                     textcoords='offset points')        
   




    

   

if __name__ == '__main__':
   
   

    max_depth = 2
    num_games = 40
    max_depth2 = 1


    player1 =  MinimaxPlayer("Minimax", 0, max_depth)
    player2 = RandomPlayer()


    #play_games(player1,player2,num_games,)

    player1 = RandomPlayer()
    player2 = MinimaxPlayer("Minimax", 1, max_depth)

    #play_games(player1,player2,num_games)
    num_games = 10
    player1 = MinimaxPlayer("Minimax_d3", 0, max_depth)
    player2 = MinimaxPlayer("Minimax_d2", 1, max_depth2)
    play_games(player1,player2,num_games)

    player1 = MinimaxPlayer("Minimax_d2", 0, max_depth2)
    player2 = MinimaxPlayer("Minimax_d3", 1, max_depth)
    play_games(player1,player2,num_games)
    










    







