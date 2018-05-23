from Grafo import Grafo
class AlgoritmoKruskal():
    def aplicarKruskal(self, grafo):
        arbol = Grafo()
        nodos = grafo.getNombres()
        for n in nodos:
            arbol.ingresarNodo(n)
        l = grafo.getAristas()
        while l:
            arcoPro = l[0]
            if (self.hayCiclo(arbol,
                              arcoPro,
                              arbol.getNodo(arcoPro.getTerminal()),
                              arcoPro.getTerminal()) == False):
                arbol.adicionarEnlace(arcoPro.getInicial(), arcoPro.getTerminal(), arcoPro.getPeso())
            del l[0]
        return arbol
        
    def hayCiclo(self, g, aVerificar, terminal,  m):
        auxiliar = terminal.getEnlaces()
        if len(auxiliar) == 0:
            return False
        if terminal.existeEnlace(aVerificar.getInicial()) != -1:
            return True
        for n in auxiliar:
            nodo = n
            if nodo.getDestino() != m:
                if self.hayCiclo(g,
                                aVerificar,
                                g.getNodo(nodo.getDestino()),
                                terminal.getNombre()):
                    return True
        return False

        
