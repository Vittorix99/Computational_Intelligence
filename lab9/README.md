# Progetto Algoritmo Genetico - README

## Autore
Il codice in questo repository è stato sviluppato con l'aiuto di Antonio Ferrigno, matricola S316467, che ha contribuito in alcune sezioni specifiche del progetto.

## Descrizione del Codice
Questo progetto implementa un algoritmo genetico per risolvere il problema OneMax. L'obiettivo è massimizzare la funzione di fitness, che è la somma dei valori in un vettore binario, cercando di ottenere tutti i bit impostati a 1. Inoltre, l'algoritmo è progettato per trovare le configurazioni di parametri che minimizzano la chiamata alla funzione di fitness.

### Parametri dell'Algoritmo
Durante l'esecuzione dell'algoritmo,viene eseguito l'algoritmo evolutivo facendo variare alcuni parametri:

- **Population Size**: La dimensione della popolazione di individui considerati durante ogni generazione.

- **Tournament Size**: Il numero di individui selezionati casualmente dalla popolazione per partecipare al torneo di selezione.

- **Convergence Rate**: La percentuale di convergenza che indica quando l'algoritmo deve fermarsi, considerando la soluzione raggiunta accettabile.

