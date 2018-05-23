from Nodo import Nodo
from Arco import Arco
class Grafo():
    def __init__(self):
        self.nombres = []
        self.nodos = []
        self.aristas = []
        
    def ingresarNodo(self, nuevoNombre):
        self.nombres.append(nuevoNombre)
        self.nodos.append([nuevoNombre, Nodo(nuevoNombre)])
        
    def adicionarEnlace(self, nodoInicial, nodoTerminal, peso):
        nuevoArco = Arco(nodoInicial, nodoTerminal, float(peso))
        indice = self.buscarIndice(nuevoArco.getPeso())
        if indice == -1:
            self.aristas.append(nuevoArco)
        else:
            self.aristas.insert(int(indice), nuevoArco)

        for nodo in self.nodos:
            if nodoInicial in nodo[0]:
                nodo[1].agregarEnlace(nodoTerminal, peso)
                break
        for nodo in self.nodos:
            if nodoTerminal in nodo[0]:
                nodo[1].agregarEnlace(nodoInicial, peso)
                break
    
    def buscarArista(self, arco):
        i = 0
        for arista in self.aristas:
            if (arco.getInicial() == arista.getInicial() and
                arco.getTerminal() == arista.getTerminal() and
                arco.getPeso() == arista.getPeso()):
                del self.aristas[i]
                return True
            i = i + 1
        return False
    
    def buscarIndice(self, peso):
        for arista in self.aristas:
            if peso < arista.getPeso():
                return self.aristas.index(arista)
        return -1
    
    def getNodos(self):
        return self.nodos
    
    def setNodos(self, nodos):
        pass
    
    def getNombres(self):
        return self.nombres
    
    def getNodo(self, nombre):
        for n in self.nodos:
            if nombre in n[0]:
                return n[1]
    
    def getAristas(self):
        return self.aristas
    
    def setAristas(self, aristas):
        self.aristas = aristas
        
    def setNombres(self, nombres):
        self.nombres = nombres
