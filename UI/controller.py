import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        dMinTxt = self._view._txtInDurata.value #str
        if dMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, valore minimo di durata non inserito!", color="red"))
            self._view.update_page()
            return

        try:
            dMinInt = int(dMinTxt) #la inserisco in un blocco try-except perché l'operazione può fallire
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, valore inserito non valido", color="red"))
            self._view.update_page()
            return

        # se arrivo qui il valore è accetabile e convertito ad intero
        self._model.buildGraph(dMinInt)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo è costituito da {nNodes} nodi e {nEdges} archi"))
        self._fillDD(self._model.getAllNodes())
        self._view.update_page()

    def handleAnalisiComp(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, album non selezionato", color="red"))
            self._view.update_page()
            return
        size, dTotCC = self._model.getInfoConnessa(self._choiceDD)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceDD} ha {size} nodi e una durata totale di {dTotCC:.3f}"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        sogliaTxt = self._view._txtInSoglia.value
        if sogliaTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, soglia massima di durata non inserita!", color="red"))
            self._view.update_page()
            return

        try:
            sogliaInt = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, valore di soglia inserito non è un intero", color="red"))
            self._view.update_page()
            return

        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare una voce dal menù", color="red"))
            self._view.update_page()
            return

        setOfNodes, sumDurate = self._model.getSetOfNodes(self._choiceDD, sogliaInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un set di album che soddisfa le specifiche, dimensione: {len(setOfNodes)}, durata totale: {sumDurate:.3f}"))
        self._view.txt_result.controls.append(ft.Text(f"Di seguito gli album che fanno parte della soluzione trovata"))
        for n in setOfNodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()


    def _fillDD(self, listOfNodes):
        listOfNodes.sort(key = lambda x:x.Title)
        listOfOptions = map(lambda x: ft.dropdown.Option(text = x.Title,
                                                         on_click=self._readDDValue,
                                                         data = x), listOfNodes)
        # la funzione map prende una funzione e un iterable, quindi la lambda function prende x e la aggiunge come opzione
        # l'iterable è la lista di nodi
        # è equivalente a fare:
        # listOfOptions = []
        # for n in listOfNode:
            #listOfOptions.append(ft.dropdown.Option(text = n.Title, on_click=self._readDDValue, data = n))

        self._view._ddAlbum.options = list(listOfOptions)

    def _readDDValue(self, e):
        # deve leggere dall'evento il valore di data
        if e.control.data is None:
           self._choiceDD = None
           print("error in reading DD")
        self._choiceDD = e.control.data

