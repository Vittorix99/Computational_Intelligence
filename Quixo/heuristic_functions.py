import numpy as np
from state import GameState,GameNode, NUM_ROWS
import itertools

BLOCK_SCORE = 10
WIN_SCORE = 100
MAX_SEQ_SCORE = 50
MIN_TARGET = 1
MAX_TARGET = 5




def valuta_symbol_advantage(board, player_symbol, opponent_symbol):
        player_count = np.sum(board == player_symbol)
        opponent_count = np.sum(board == opponent_symbol) 
        empty_count = np.sum (board == -1)



        symbol_advantage = (player_count - opponent_count) * map_to_range(empty_count)
        return symbol_advantage
            
def valuta_controllo_scacchiera(state:GameState):
            #Questa funzione valuta per r
            # ighe colonne e diagonali quale giocatore ha più simboli consecutivi
            


            player_symbol = state.current_player
            opponent_symbol = 1 - player_symbol
            score = 0

            for i in range(NUM_ROWS):
                
                score+= scala_punteggio(max_seq_in_line(state.board[i,:], player_symbol)) - scala_punteggio(max_seq_in_line(state.board[i,:], opponent_symbol))
                
                score+= scala_punteggio(max_seq_in_line(state.board[:,i], player_symbol)) - scala_punteggio(max_seq_in_line(state.board[:,i], opponent_symbol))
        
            score+= scala_punteggio(max_seq_in_line(state.board.diagonal(), player_symbol)) - scala_punteggio(max_seq_in_line(state.board.diagonal(), opponent_symbol))
            score+= scala_punteggio(max_seq_in_line(np.fliplr(state.board).diagonal(), player_symbol)) - scala_punteggio(max_seq_in_line(np.fliplr(state.board).diagonal(), opponent_symbol))


            return score


def valuta_winning_score(node  : GameNode, player_symbol, opponent_symbol):
        state = node.state  
        winner = state.winner

        winningscore = WIN_SCORE -node.step if winner == player_symbol else -WIN_SCORE +node.step if winner == opponent_symbol else 0
       
        return winningscore



def valuta_blocco_avversario(nodo, player_symbol, opponent_symbol):
    """
    Valuta se una mossa ha bloccato una potenziale linea vincente dell'avversario.
    
    Args:
    nodo (GameNode): Il nodo corrente nel gioco.
    player_symbol (int): Il simbolo del giocatore corrente.
    opponent_symbol (int): Il simbolo dell'avversario.

    Returns:
    int: Il punteggio basato sull'efficacia del blocco delle mosse dell'avversario.
    """
    if nodo.parent is None:
        return 0  # Non c'è uno stato precedente da confrontare

    parent_state = nodo.parent.state
    current_state = nodo.state
    punteggio_blocco = 0

    # Valuta righe, colonne e diagonali per potenziali blocchi
    for i in range(NUM_ROWS):
        punteggio_blocco += valuta_cambiamento_linea(parent_state.board[i, :], current_state.board[i, :], player_symbol, opponent_symbol)
        punteggio_blocco += valuta_cambiamento_linea(parent_state.board[:, i], current_state.board[:, i], player_symbol, opponent_symbol)

    punteggio_blocco += valuta_cambiamento_linea(parent_state.board.diagonal(), current_state.board.diagonal(), player_symbol, opponent_symbol)
    punteggio_blocco += valuta_cambiamento_linea(np.fliplr(parent_state.board).diagonal(), np.fliplr(current_state.board).diagonal(), player_symbol, opponent_symbol)

    return punteggio_blocco

def valuta_cambiamento_linea(parent_line, current_line, player_symbol, opponent_symbol):
    """
    Valuta un cambiamento in una linea specifica (riga, colonna o diagonale) dallo stato
    genitore allo stato corrente per determinare se una mossa ha bloccato un avversario.
    
    Args:
    parent_line (array): La linea nello stato genitore.
    current_line (array): La stessa linea nello stato corrente.
    player_symbol (int): Il simbolo del giocatore corrente.
    opponent_symbol (int): Il simbolo dell'avversario.

    Returns:
    int: Punteggio basato su se la mossa ha bloccato o creato una linea pericolosa.
    """
    parent_max_seq = max_seq_in_line(parent_line, opponent_symbol)
    current_max_seq = max_seq_in_line(current_line, opponent_symbol)

    if parent_max_seq == 4 and current_max_seq < 4:
        return BLOCK_SCORE  # Punteggio per aver bloccato una linea
    elif current_max_seq == 4:
        return -BLOCK_SCORE  # Penalità per aver creato una nuova linea pericolosa
    return 0

def max_seq_in_line(line, symbol):
    """
    Trova la massima sequenza di simboli consecutivi in una linea.
    
    Args:
    line (array): Una riga, colonna o diagonale della scacchiera.
    symbol (int): Il simbolo da cercare nella sequenza.

    Returns:
    int: La lunghezza della massima sequenza consecutiva del simbolo.
    """
    return max((len(list(group)) for key, group in itertools.groupby(line) if key == symbol), default=0)












def max_seq_in_line(line, player_symbol):
             lengths = [len(list(group)) for key, group in itertools.groupby(line) if key == player_symbol]
             return np.max(lengths) if lengths else 0


def scala_punteggio(lunghezza):
            if lunghezza<5:
                return (lunghezza/5)*MAX_SEQ_SCORE
            else:
                return WIN_SCORE     #caso di vittoria
            


def map_to_range(num):
    min_source = 0
    max_source = 25
    

    if min_source <= num <= max_source:
        return MIN_TARGET + (num - min_source) / (max_source - min_source) * (MAX_TARGET - MIN_TARGET)
    else:
        raise ValueError("Il numero deve essere compreso tra 1 e 23")


