from model.model import Model

m = Model()
m.buildGraph(120) #passiamo una durata in minuti
n, e = m.getGraphDetails()
print(f"Numero di nodi: {n}, numero di archi: {e}")