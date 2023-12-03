from abc import abstractmethod

class AbstractProblem:
    def __init__(self):
        self._calls = 0

    @property
    @abstractmethod
    def x(self):
        pass

    @property
    def calls(self):
        return self._calls
        

    @staticmethod
    def onemax(genome):
        return sum(bool(g) for g in genome)

    def __call__(self, genome):
        self._calls += 1
        fitnesses = sorted((AbstractProblem.onemax(genome[s::self.x]) for s in range(self.x)), reverse=True)
        val = fitnesses[0] - sum(f*(.1 ** (k+1)) for k, f in enumerate(fitnesses[1:]))
        return val / len(genome) * self.x

def make_problem(a):
    class Problem(AbstractProblem):
        @property
        @abstractmethod
        def x(self):
            return a

    return Problem()


#Il valore di fitness finale viene calcolato come il fitness massimo 
# meno la somma dei fitness restanti, ciascuno moltiplicato per un fattore di penalità che diminuisce esponenzialmente.
#  Questo valore viene poi normalizzato dividendo per la lunghezza del genoma e moltiplicando per self.x.


#In sintesi, questo metodo calcola un valore di fitness che premia i genomi con un alto numero di '1' in una sezione,
#  ma penalizza i genomi che hanno un alto numero di '1' solo in una sezione e non nelle altre.