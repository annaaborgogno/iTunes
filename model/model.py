import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allNodi = []
        self._grafo = nx.Graph()
        self._idMapAlbum = {}
        self._bestSet = {}
        self._maxLen = 0

    def getSetOfNodes(self, a1, soglia):
        self._bestSet = {} #ogni volta che cerchiamo una soluzione partiamo da 0
        self._maxLen = 0

        parziale = {a1}
        cc = nx.node_connected_component(self._grafo, a1)
        #essendo un set gli elementi sono distinti, stiamo facendo una ricorsione sui nodi
        # tolgo comunque gli elementi che ho già provato ad inserire per alleggerire il carico e non fare operazioni inutili
        cc.remove(a1) #risparmio un'iterazione del ciclo
        for n in cc:
            #richiamo la ricorsione
            parziale.add(n) #add perché è un set
            cc.remove(n)
            self._ricorsione(parziale, cc, soglia) #passo i nodi che devo provare ad inserire e la soglia
            cc.add(n)
            parziale.remove(n) #backtracking
        return self._bestSet, self._getDurataTot(self._bestSet) #durata che deve essere inferiore alla soglia

    def _ricorsione(self, parziale, rimanenti, soglia):
        # i rimanenti sono i nodi della componente connessa che ancora posso aggiungere
        #1) verifico che parziale sia una soluzione ammissibile, ovvero se viola i vincoli --> se è vera, esco (condizione di terminazione)
        if self._getDurataTot(parziale) > soglia:
            return
        #2) se parziale soddisfa i criteri allora verifico se è migliore di bestSet --> non è condizione di terminazione
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)
        #3) aggiungo e faccio ricorsione
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale, rimanenti, soglia)
            parziale.remove(n)
            rimanenti.add(n)
            #per rimanenti faccio backtracking al contrario
            # ciclo su una lista che è sempre più corta, risparmiando tempo


    def buildGraph(self, durataMin):
        self._grafo.clear() #pulire sempre ol grafo altrimenti se si fanno più grafi sequenzialmente non funziona correttamente
        self._allNodi = DAO.getAlbums(durataMin)
        self._grafo.add_nodes_from(self._allNodi)
        self._idMapAlbum = {n.AlbumId: n for n in self._allNodi} #contiene solo i nodi presenti nel grafo
        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges) #perché ho già controllato che gli archi sono già nodi che sono nella mappa

    def getInfoConnessa(self, a1):
        cc = nx.node_connected_component(self._grafo, a1) #componente connessa che contiene a1
        return len(cc), self._getDurataTot(cc)  # dimensione della componente connessa

    def _getDurataTot(self, listOfNodes):
        sumDurata = 0
        for n in listOfNodes:
            sumDurata += n.dTot
        return sumDurata
        #return sum([n.dTot for n in listOfNodes]) con la list comprehension ne fa la somma mettendo tutto in una lista

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes()) #metodo che mi da un NodeView che io converto in una lista