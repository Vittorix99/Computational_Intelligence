# README

## Progetto di Laboratorio: Algoritmo Genetico per il Gioco di Nim

Questo progetto di laboratorio è stato svolto in collaborazione con Antonio Ferrigno (Matricola: xxxx) e Martina Martina (Matricola: xxxxx). Nel corso di questo lavoro, abbiamo implementato un algoritmo genetico per il gioco di Nim, prendendo ispirazione e utilizzando pezzi di codice forniti da Antonio Ferrigno.

### Descrizione del Codice

Il codice implementato funziona nel seguente modo:

1. **Inizializzazione della Popolazione:** Una popolazione di agenti viene inizializzata, ognuno con un genoma composto da due parti. La prima parte del genoma indica il peso dato a ciascuna strategia (inventate durante lo sviluppo del progetto), mentre la seconda parte indica il peso da assegnare a ogni riga quando si gioca con due strategie specifiche, corrispondenti alle caselle 0 e 1 della prima parte del genoma.

2. **Strategie Ottimali:** Tra le strategie, quella associata alla prima casella del genoma è ottimale, poiché porta la somma Nim a 0. Le ultime strategie del genoma sono più randomiche.

3. **Algoritmo Genetico:** A ogni generazione, ogni agente viene valutato. Il 50% dei giocatori peggiori viene scartato, mentre un nuovo 25% viene creato tramite crossover o mutazione del genoma, partendo da una selezione randomica del 10% dei giocatori più forti.

4. **Convergenza alla Strategia Ottimale:** Dopo un numero di generazioni, l'esperimento dimostra che l'algoritmo genetico converge a una stringa genoma_strategy con un 1 nella prima casella e tutti 0 nelle caselle successive. Ciò avviene poiché le strategie selezionate si avvicinano progressivamente a questa configurazione ottimale.

### Istruzioni per l'esecuzione del Codice

Per eseguire il codice, seguire i seguenti passaggi:

1. [Installare le dipendenze necessarie](link-alle-istruzioni-di-installazione).

2. Eseguire il file principale del progetto: `main.py`.

3. Osservare l'evoluzione delle strategie e il raggiungimento della configurazione ottimale nel corso delle generazioni.

### Ringraziamenti

Desideriamo esprimere la nostra gratitudine a Antonio Ferrigno per la collaborazione e il contributo al progetto.

---
